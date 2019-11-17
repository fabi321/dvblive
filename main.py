import logging
from fetch_init import fetch_init, output_format


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s [%(funcName)s]: %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%S')

init_data: output_format = fetch_init()
