import logging

from fetch_init import fetch_init
# from fetch_live import fetch_live
from generate_json import generate_json

logging.basicConfig(level=logging.WARNING, format='[%(levelname)s] %(asctime)s %(name)s [%(funcName)s]: %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%S')

debug: bool = False
fetch_init(debug)
abschnitte, haltestellen = generate_json()
with open('frontend/abschnitte.json', 'w') as f:
    f.write(abschnitte)
with open('frontend/haltestelle.json', 'w') as f:
    f.write(haltestellen)
# while True:
#    fetch_live()
#    abschnitte, haltestellen = generate_json()
#    with open('frontend/abschnitte.json', 'w') as f:
#        f.write(abschnitte)
#    with open('frontend/haltestelle.json', 'w') as f:
#        f.write(haltestellen)
#    time.sleep(30)
