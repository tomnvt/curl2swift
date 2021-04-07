import sys
import subprocess
from urllib.parse import urlparse
from collections import namedtuple
from ast import literal_eval

from curl2swift.processing.create_request import create_request
from curl2swift.processing.get_response_json import get_response_json
from curl2swift.processing.prepare_enum_cases import prepare_enum_cases
from curl2swift.utils.logger import logging
from curl2swift.parsing.get_request_properties import get_request_properties

ParsedContent = namedtuple(
    "ParsedContent",
    [
        "url",
        "method",
        "path",
        "query_params",
        "headers",
        "param_names",
        "path_param_rows",
        "response_json",
        "header_rows",
        "body_param_rows",
    ],
)


def get_curl():
    logging.info("Reading curl from --curl option")

    if "--curl" in sys.argv:
        index = sys.argv.index("--curl")
        curl = sys.argv[index + 1]
        logging.info("Got cURL from option: " + curl)
    else:
        logging.info("--curl option not used")
        logging.info("Reading curl from clipboard")
        curl = subprocess.check_output(
            ["pbpaste", "r"], stdin=subprocess.PIPE
        ).decode("utf-8")

    curl = curl.replace("--location", "")
    curl = curl.replace("-v", "")
    curl = curl.replace("--request", "-X")
    curl = curl.replace("\\\n", "")
    logging.info("cURL after cleanup: " + curl)
    return curl


def get_parameter_names(request_properties):
    if request_properties.data:
        data = request_properties.data
        if "{" in data:
            data = literal_eval(data)
            return [[param, data[param]] for param in data]
        else:
            data_with_ampersands = data.replace(";", "&").split("&")
            return [param.split("=") for param in data_with_ampersands]
    elif request_properties.data_urlencode:
        return [
            param.split("=") for param in request_properties.data_urlencode
        ]
    return []


def get_request_content(parser):
    curl = get_curl()

    test_curl = "curl -i https://api.github.com/users/defunkt"
    try:
        logging.info("Parsing cURL")
        request_properties = get_request_properties(curl, parser)
    except:  # noqa: E722
        logging.error("Parsing failed (see usage above)")
        logging.info("Falling back to test cURL")
        curl = test_curl
        request_properties = get_request_properties(test_curl, parser)

    logging.info("Transforming cURL to Python request object")
    path_param_rows = []  # NOTE: path params are not yet supported
    param_names = []
    method = request_properties.method
    parsed_url = urlparse(request_properties.url)

    param_names = get_parameter_names(request_properties)
    headers = request_properties.headers
    url = parsed_url.scheme + "://" + parsed_url.netloc
    path = parsed_url.path
    if parsed_url.query:
        query_params = {
            param.split("=")[0]: param.split("=")[1]
            for param in parsed_url.query.split("&")
        }
    else:
        query_params = None

    logging.info("URL: " + url)
    logging.info("Found method: " + method)
    logging.info("Found path: " + path)
    logging.info("Found query params: " + str(query_params))
    logging.info("Found headers: " + str(headers))
    logging.info("Found body params: " + str(param_names))

    request_code = create_request(request_properties)
    response_json = get_response_json(request_code)
    header_rows = prepare_enum_cases(list(headers.keys()), "header")
    body_param_rows = prepare_enum_cases(param_names, "param")

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
        body_param_rows,
    )
    logging.info("Content parsed.")
    return content
