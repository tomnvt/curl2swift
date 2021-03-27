import sys

from curl2swift.utils.logger import logging


def get_request_name_and_description():
    args = sys.argv[1:]
    try:
        request_name = args[0]
    except IndexError:
        logging.warning("Request name missing.")
        request_name = 'Test'

    try:
        description = args[1]
    except IndexError:
        logging.warning('Request description missing.')
        description = 'Add description'
    
    return request_name, description
