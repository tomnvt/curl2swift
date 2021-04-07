from curl2swift.parsing.get_parser import get_curl_parser
from curl2swift.parsing.parse_content import get_request_content
from curl2swift.parsing.get_request_name_and_description import (
    get_request_name_and_description,
)
from curl2swift.processing.create_response_model import create_response_model
from curl2swift.processing.process_test_template import process_test_template
from curl2swift.processing.process_request_template import (
    process_request_template,
)


def parse_inputs():
    parser = get_curl_parser()
    request_name, description = get_request_name_and_description()
    request_content = get_request_content(parser)
    return request_name, description, request_content


def process_inputs(request_name, description, request_content):
    response_model = create_response_model(request_content.response_json)
    process_request_template(
        request_name, description, request_content, response_model
    )
    process_test_template(request_name, request_content)


def run_main_process():
    request_name, description, request_content = parse_inputs()
    process_inputs(request_name, description, request_content)
