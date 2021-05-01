from subprocess import SubprocessError
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

cached_response = {}


def parse_inputs(user_input, should_make_request=False):
    global cached_response
    parser = get_curl_parser()
    if user_input:
        request_name, description = user_input.request_name, user_input.description
    else:
        request_name, description = get_request_name_and_description()
    request_content, response_json = get_request_content(
        parser, user_input.curl, should_make_request
    )
    if should_make_request:
        cached_response = response_json
    else:
        response_json = cached_response
    return request_name, description, request_content, response_json


def process_inputs(
    request_name, description, request_content, response_json, is_windowed
):
    response_model = create_response_model(response_json)
    request = process_request_template(
        request_name, description, request_content, response_model
    )

    if not is_windowed:
        should_copy = input("Copy output to clipboard? [y/n]\n")

        if should_copy == "y":
            SubprocessError.run("pbcopy", universal_newlines=True, input=request)

    unit_test = process_test_template(request_name, request_content)

    if not is_windowed:
        should_copy = input("Copy output to clipboard? [y/n]\n")

        if should_copy == "y":
            SubprocessError.run("pbcopy", universal_newlines=True, input=unit_test)

    return request, unit_test


def run_main_process(user_input, is_windowed=False, should_make_request=False):
    request_name, description, request_content, response_json = parse_inputs(
        user_input, should_make_request
    )
    return process_inputs(
        request_name, description, request_content, response_json, is_windowed
    )
