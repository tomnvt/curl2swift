# __main__.py
from curl2swift.get_parser import get_parser
from curl2swift.process_test_template import process_test_template
from curl2swift.process_request_template import process_request_template
from curl2swift.parse_content import parse_content
from curl2swift.prepare_enum_cases import prepare_enum_cases


def main():
    parser = get_parser()

    curl, content = parse_content(parser)

    header_rows = prepare_enum_cases(content.header_names, 'header')
    body_param_rows = prepare_enum_cases(content.param_names, 'param')

    process_request_template(curl, parser, content, header_rows, body_param_rows)
    process_test_template(header_rows, body_param_rows, content)


if __name__ == "__main__":
    main()
