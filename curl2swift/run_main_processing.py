from curl2swift.parsing.get_parser import get_curl_parser
from curl2swift.parsing.parse_content import parse_curl
from curl2swift.parsing.get_request_name_and_description import get_request_name_and_description

from curl2swift.processing.create_request import create_request
from curl2swift.processing.get_response_json import get_response_json
from curl2swift.processing.create_response_model import create_response_model
from curl2swift.processing.process_test_template import process_test_template
from curl2swift.processing.process_request_template import process_request_template
from curl2swift.processing.prepare_enum_cases import prepare_enum_cases


def run_main_processing():
    parser = get_curl_parser()

    request_name, description = get_request_name_and_description()
    curl, content = parse_curl(parser)
    header_rows = prepare_enum_cases(list(content.headers.keys()), 'header')
    body_param_rows = prepare_enum_cases(content.param_names, 'param')

    request_code = create_request(curl, parser)
    response_json = get_response_json(request_code)
    response_model = create_response_model(response_json)
    process_request_template(
        request_name, description, content, header_rows, body_param_rows, response_model
    )
    process_test_template(request_name, header_rows, body_param_rows, content)
