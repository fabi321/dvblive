from typing import Sequence, Any, List, TypeVar

import ZODB.DB
import ZODB.config
import transaction
from BTrees.IOBTree import BTree
from ZODB.Connection import Connection
from persistent import Persistent
from persistent.dict import PersistentDict

from Classes.Utilities.db_config import zodb_conf


class Manager(Persistent):
    _db_config: str = zodb_conf
    _T: TypeVar = TypeVar('_T')
    _U: TypeVar = TypeVar('_U')

    def __init__(self, name: str, key: _U, value: _T):
        self._name: str = name
        self._value = value
        self._highest_index = 0
        self._mappings: PersistentDict[str, int] = PersistentDict()
        db: ZODB.DB = ZODB.config.databaseFromString(self._db_config)
        connection: Connection = db.open()
        try:
            connection.root()[self._name]
        except KeyError:
            connection.root()[self._name] = BTree()
            transaction.commit()
        connection.close()
        db.close()

    def __getitem__(self, item: _U) -> _T:
        db: ZODB.DB = ZODB.config.databaseFromString(self._db_config)
        connection: Connection = db.open()
        items = connection.root()[self._name]
        item = items[self._mappings[item]]
        db.close()
        connection.close()
        return item

    def __add__(self, other: _T):
        self.append(other)
        return self

    def append(self, other: _T, key=None):
        if not isinstance(other, type(self._value)):
            raise NotImplementedError('Tried to add ' + str(type(self._value)) + ' with ' + str(type(other)) + '.')
        db: ZODB.DB = ZODB.config.databaseFromString(self._db_config)
        connection: Connection = db.open()
        items = connection.root()[self._name]
        while self._highest_index in self._mappings.keys():
            self._highest_index += 1
        items[self._highest_index] = other
        self._mappings[key if key else str(other)] = self._highest_index
        self._highest_index += 1
        transaction.commit()
        connection.close()
        db.close()

    def __len__(self) -> int:
        return len(self._mappings)

    def __setitem__(self, key, value: _T):
        if key in self._mappings.keys():
            db: ZODB.DB = ZODB.config.databaseFromString(self._db_config)
            connection: Connection = db.open()
            items = connection.root()[self._name]
            items[self._mappings[key]] = value
            transaction.commit()
            db.close()
            connection.close()
        else:
            self.append(value, key=key)

    def __contains__(self, item: _T) -> bool:
        return item in self._mappings.keys()

    def __iter__(self):
        return iter(self._mappings)

    def keys(self) -> List[_U]:
        return list(self._mappings.keys())

    def values(self) -> List[_T]:
        db: ZODB.DB = ZODB.config.databaseFromString(self._db_config)
        connection: Connection = db.open()
        items = connection.root()[self._name].values()
        db.close()
        connection.close()
        return items

    def from_list(self, in_list: Sequence[_U]) -> List[_T]:
        out_list: List[Any] = [self[i] for i in in_list]
        return out_list
