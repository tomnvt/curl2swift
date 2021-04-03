from collections import namedtuple
from ast import literal_eval
from curl2swift.processing.create_request import create_request
from curl2swift.processing.get_response_json import get_response_json
from curl2swift.processing.prepare_enum_cases import prepare_enum_cases
from urllib.parse import urlparse
import sys

import clipboard

from curl2swift.utils.logger import logging
from curl2swift.parsing.parse_context import parse_context

ParsedContent = namedtuple('ParsedContent', ('\
    url,\
    method, \
    path,\
    query_params,\
    headers,\
    param_names,\
    path_param_rows,\
    response_json,\
    header_rows,\
    body_param_rows'
))

def get_curl():
    logging.info('Reading curl from --curl option')
    arguments = ' '.join(sys.argv)
    if '--curl' in sys.argv:
        index = sys.argv.index('--curl')
        curl = sys.argv[index + 1]
        logging.info('Got cURL from option: ' + curl)
    else:
        logging.info('--curl option not used')
        logging.info('Reading curl from clipboard')
        curl = clipboard.paste()

    curl = curl.replace('--location', '')
    curl = curl.replace('-v', '')
    curl = curl.replace('--request', '-X')
    curl = curl.replace('\\\n', '')
    logging.info('cURL after cleanup: ' + curl)
    return curl


def get_parameter_names(context):
    if context.data:
        data = context.data
        if '{' in data:
            data = literal_eval(data)
            return [[param, data[param]] for param in data]
        else:
            return [param.split('=') for param in data.replace(';', '&').split('&')]
    elif context.data_urlencode:
        return [param.split('=') for param in context.data_urlencode]
    return []

def get_request_content(parser):
    curl = get_curl()

    TEST_CURL = "curl -i https://api.github.com/users/defunkt"
    try:
        logging.info('Parsing cURL')
        context = parse_context(curl, parser)
    except:
        logging.error('Parsing failed (see usage above)')
        logging.info('Falling back to test cURL')
        curl = TEST_CURL
        context = parse_context(TEST_CURL, parser)

    logging.info('Transforming cURL to Python request object')
    path_param_rows = [] # NOTE: path params are not yet supported
    param_names = []
    method = context.method
    parsed_url = urlparse(context.url)

    param_names = get_parameter_names(context)
    headers = context.headers
    url = parsed_url.scheme + '://' + parsed_url.netloc
    path = parsed_url.path
    query_params = {param.split('=')[0]: param.split('=')[1]\
        for param in parsed_url.query.split('&')} \
        if parsed_url.query else None

    logging.info('URL: ' + url)
    logging.info('Found method: ' + method)
    logging.info('Found path: ' + path)
    logging.info('Found query params: ' + str(query_params))
    logging.info('Found headers: ' + str(headers))
    logging.info('Found body params: ' + str(param_names))

    request_code = create_request(context)
    response_json = get_response_json(request_code)
    header_rows = prepare_enum_cases(list(headers.keys()), 'header')
    body_param_rows = prepare_enum_cases(param_names, 'param')

    content = ParsedContent(
        url, 
        method, 
        path, 
        query_params, 
        headers, 
        param_names, 
        path_param_rows, 
        response_json, 
        header_rows, 
        body_param_rows
    )
    logging.info("Content parsed.")
    return content
