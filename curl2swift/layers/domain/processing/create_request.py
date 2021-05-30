from curl2swift.utils.dict_to_pretty_string import dict_to_pretty_string


BASE_INDENT = " " * 4


def create_request(parsed_context, path_params):
    data_token = ""
    if parsed_context.data:
        data_token = "{}data='{}',\n".format(BASE_INDENT, parsed_context.data)

    if parsed_context.data_urlencode:
        data_token = "{}data='{}',\n".format(
            BASE_INDENT, "&".join(parsed_context.data_urlencode)
        )

    verify_token = ""
    if parsed_context.verify:
        verify_token = "\n{}verify=False".format(BASE_INDENT)

    auth_data = "{}auth={}".format(BASE_INDENT, parsed_context.auth)
    headers = dict_to_pretty_string(parsed_context.headers)
    cookies = dict_to_pretty_string(parsed_context.cookies)

    url = parsed_context.url
    for param in path_params:
        path_param_mark = "{" + param + "}"
        if path_param_mark in url:
            url = url.replace(path_param_mark, path_params[param])

    formatter = {
        "method": parsed_context.method,
        "url": url,
        "data_token": data_token,
        "headers_token": "{}headers={}".format(BASE_INDENT, headers),
        "cookies_token": "{}cookies={}".format(BASE_INDENT, cookies),
        "security_token": verify_token,
        "auth": auth_data,
    }

    return """requests.{method}("{url}",
{data_token}{headers_token},
{cookies_token},
{auth},{security_token}
)""".format(
        **formatter
    )
