from curl2swift.utils.dict_to_pretty_string import dict_to_pretty_string
from curl2swift.parsing.get_request_properties import get_request_properties


BASE_INDENT = " " * 4


def create_request(parsed_context):
    data_token = ''
    if parsed_context.data:
        data_token = '{}data=\'{}\',\n'\
            .format(BASE_INDENT, parsed_context.data)

    if parsed_context.data_urlencode:
        data_token = '{}data=\'{}\',\n'\
            .format(BASE_INDENT, '&'.join(parsed_context.data_urlencode))

    verify_token = ''
    if parsed_context.verify:
        verify_token = '\n{}verify=False'.format(BASE_INDENT)

    auth_data = "{}auth={}".format(BASE_INDENT,parsed_context.auth)

    formatter = {
        'method': parsed_context.method,
        'url': parsed_context.url,
        'data_token': data_token,
        'headers_token': "{}headers={}"\
            .format(BASE_INDENT, dict_to_pretty_string(parsed_context.headers)),
        'cookies_token': "{}cookies={}"\
            .format(BASE_INDENT, dict_to_pretty_string(parsed_context.cookies)),
        'security_token': verify_token,
        'auth': auth_data
    }

    return """requests.{method}("{url}",
{data_token}{headers_token},
{cookies_token},
{auth},{security_token}
)""".format(**formatter)
