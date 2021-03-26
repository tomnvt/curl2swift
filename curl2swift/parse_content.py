from collections import namedtuple

import pyp3rclip
from ast import literal_eval
import sys
from urllib.parse import urlparse
import logging
from curl2swift.parse_context import parse_context

ParsedContent = namedtuple('ParsedContent', 'request_name, description, url, method, path, query_params, headers, header_names, param_names, path_param_rows')


def parse_content(parser):
    logging.info('Parsing content')
    test_curl = "curl -i https://api.github.com/users/defunkt"

    curl = pyp3rclip.paste()
    curl = curl.replace('--location', '')
    curl = curl.replace('-v', '')
    curl = curl.replace('--request', '-X')
    curl = curl.replace('\\\n', '')

    try:
        context = parse_context(curl, parser)
    except:
        logging.error('Parsing failed')
        curl = test_curl
        context = parse_context(test_curl, parser)
    path_param_rows = []
    param_names = []
    method = context.method
    parsed_url = urlparse(context.url)

    if context.data:
        data = context.data
        if '{' in data:
            data = literal_eval(data)
            param_names = [[param, data[param]] for param in data]
        else:
            param_names = [param.split('=') for param in data.replace(';', '&').split('&')]
    elif context.data_urlencode:
        param_names = [param.split('=') for param in context.data_urlencode]
    headers = context.headers
    url = parsed_url.scheme + '://' + parsed_url.netloc
    path = parsed_url.path
    query_params = {param.split('=')[0]: param.split('=')[1] for param in parsed_url.query.split('&')} \
        if parsed_url.query else None

    header_names = list(headers.keys())

    args = sys.argv[1:]
    try:
        request_name = args[0]
    except IndexError:
        logging.error("Request name missing.")
        request_name = 'Test'
    
    try:
        description = args[1]
    except IndexError:
        logging.warning('Request description missing.')
        description = 'Add description'

    logging.info('URL: ' + url)
    logging.info('Request name: ' + request_name)
    logging.info('Found method: ' + method)
    logging.info('Found path: ' + path)
    logging.info('Found query params: ' + str(query_params))
    logging.info('Found path params: ' + str(path_param_rows))
    logging.info('Found headers: ' + str(header_names))
    logging.info('Found body params: ' + str(param_names))

    content = ParsedContent(request_name, description, url, method, path, query_params, headers, header_names, param_names, path_param_rows)
    return curl, content
