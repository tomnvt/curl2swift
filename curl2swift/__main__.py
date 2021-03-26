# __main__.py
from curl2swift.create_request import create_request
from curl2swift.get_response_json import get_response_json
from curl2swift.create_response_model import create_response_model
import logging

from curl2swift.get_parser import get_parser
from curl2swift.process_test_template import process_test_template
from curl2swift.process_request_template import process_request_template
from curl2swift.parse_content import parse_content
from curl2swift.prepare_enum_cases import prepare_enum_cases
import curl2swift.logger as logger

def main():
    logger.setup()
    parser = get_parser()

    curl, content = parse_content(parser)

    header_rows = prepare_enum_cases(content.header_names, 'header')
    body_param_rows = prepare_enum_cases(content.param_names, 'param')

    request_code = create_request(curl, parser)
    response_json = get_response_json(request_code)
    response_model = create_response_model(response_json)
    process_request_template(content, header_rows, body_param_rows, response_model)
    process_test_template(header_rows, body_param_rows, content)


if __name__ == "__main__":
    main()
