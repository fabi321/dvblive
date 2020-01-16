from typing import List, TypeVar

T = TypeVar('T')


class MergeableList(List[T], list):
    def __init__(self, mergeable_list: List[T]):
        list.__init__(self)
        for i in mergeable_list:
            self.append(i)

    def merge(self, other):
        if not isinstance(other, MergeableList):
            raise NotImplementedError('Tried to merge MergeableList with ' + str(type(other)))
        for i in other:
            if self.__contains__(i):
                self.__setitem__(self.index(i), self.__getitem__(self.index(i)) + i)
            else:
                self.append(i)
