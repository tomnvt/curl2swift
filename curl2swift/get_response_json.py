import requests

_response_json = ''

def get_response_json(request_code):
    exec('global _response_json\n_response_json = (' + request_code + '.json())')
    return _response_json
