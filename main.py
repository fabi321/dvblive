import logging
from fetch_init import fetch_init, output_format
from generate_json import generate_json


logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(name)s [%(funcName)s]: %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%S')

debug: bool = False
init_data: output_format = fetch_init(debug)
abschnitte, haltestellen = generate_json(init_data)
with open('frontend/abschnitte.json', 'w') as f:
    f.write(abschnitte)
with open('frontend/haltestelle.json', 'w') as f:
    f.write(haltestellen)