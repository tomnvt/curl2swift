from collections import OrderedDict, namedtuple
from http import cookies
import re
import shlex

RequestProperties = namedtuple('RequestProperties', [
    'method', 'url', 'data', 'data_urlencode', 'headers', 'cookies', 'verify', 'auth'
])


def parse_context(curl_command, parser):
    method = "get"

    tokens = shlex.split(curl_command)
    parsed_args = parser.parse_args(tokens)
    post_data = parsed_args.data or parsed_args.data_binary

    if post_data:
        method = 'post'

    data_urlencoded = parsed_args.data_urlencode

    if parsed_args.X:
        method = parsed_args.X.lower()

    cookie_dict = OrderedDict()
    quoted_headers = OrderedDict()

    for curl_header in parsed_args.header:
        if curl_header.startswith(':'):
            occurrence = [m.start() for m in re.finditer(':', curl_header)]
            header_key, header_value = curl_header[:occurrence[1]], curl_header[occurrence[1] + 1:]
        else:
            header_key, header_value = curl_header.split(":", 1)

        if header_key.lower().strip("$") == 'cookie':
            cookie = cookies.SimpleCookie(header_value)
            for key in cookie:
                cookie_dict[key] = cookie[key].value
        else:
            quoted_headers[header_key] = header_value.strip()

    user = parsed_args.user
    if parsed_args.user:
        user = tuple(user.split(':'))

    return RequestProperties(
        method=method,
        url=parsed_args.url,
        data=post_data,
        headers=quoted_headers,
        cookies=cookie_dict,
        verify=parsed_args.insecure,
        auth=user,
        data_urlencode=data_urlencoded
    )
