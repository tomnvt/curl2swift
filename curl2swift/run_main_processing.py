from curl2swift.parsing.get_parser import get_curl_parser
from curl2swift.parsing.parse_content import get_request_content
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
    content = get_request_content(parser)

    response_model = create_response_model(content.response_json)
    process_request_template(request_name, description, content, response_model)
    process_test_template(request_name, content)
