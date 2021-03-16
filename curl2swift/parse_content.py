from collections import namedtuple

import pyp3rclip
from ast import literal_eval
import sys
from curl2swift.parse_context import parse_context

ParsedContent = namedtuple('ParsedContent', 'request_name, description, url, method, path, headers, header_names, param_names, path_param_rows')


def parse_content(parser):
    test_curl = "curl -i https://api.github.com/users/defunkt"
    curl = pyp3rclip.paste()
    curl = curl.replace('--location', '')
    curl = curl.replace('--request', '-X')
    curl = curl.replace('\\\n', '')

    try:
        context = parse_context(curl, parser)
    except:
        curl = test_curl
        context = parse_context(test_curl, parser)
    path_param_rows = []
    param_names = []
    method = context.method
    whole_url = context.url
    if context.data:
        data = context.data
        if '{' in data:
            data = literal_eval(data)
            param_names = [[param, data[param]] for param in data]
        else:
            param_names = [param.split('=') for param in data.split('&')]
    elif context.data_urlencode:
        param_names = [param.split('=') for param in context.data_urlencode]
    headers = context.headers
    part_after_domain = whole_url.split('https://')[1]
    url = 'https://' + part_after_domain.split('/')[0]
    path = '/' + '/'.join(part_after_domain.split('/')[1:])

    header_names = list(headers.keys())

    args = sys.argv[1:]
    try:
        request_name = args[0]
    except IndexError:
        print("Request name missing.")
        request_name = 'Test'
    
    try:
        description = args[1]
    except IndexError:
        print('Request description missing.')
        description = '/// Add description'

    print('URL: ', url)
    print('Request name:' , request_name)
    print('Found method: ' + method)
    print('Found p§th: ' + path)
    print('Found path params: ' + str(path_param_rows))
    print('Found headers: ' + str(header_names))
    print('Found body params: ' + str(param_names))

    content = ParsedContent(request_name, description, url, method, path, headers, header_names, param_names, path_param_rows)
    return curl, content
