from curl2swift.utils.pprint_color import pprint_color
import subprocess
from sys import path
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


def parse_inputs(user_input, should_make_request=False, path_params={}):
    global cached_response
    parser = get_curl_parser()
    if user_input:
        request_name, description = user_input.request_name, user_input.description
    else:
        request_name, description = get_request_name_and_description()
    request_content, response_json = get_request_content(
        parser,
        user_input.curl if user_input else None,
        should_make_request,
        path_params,
    )
    if should_make_request:
        cached_response = response_json
    else:
        response_json = cached_response
    return request_name, description, request_content, response_json


def process_inputs(
    request_name,
    description,
    request_content,
    response_json,
    is_windowed,
    dynamic_values={},
    path_params={},
    use_dynamic_values_setter=False,
):
    response_model = create_response_model(response_json)
    request = process_request_template(
        request_name,
        description,
        request_content,
        response_model,
        dynamic_values,
        path_params,
    )

    if not is_windowed:
        print("\n" + "- " * 9)
        print("GENERATED REQUEST:")
        print("" + "- " * 9 + "\n")
        pprint_color(request)
        print("\n" + "- " * 12)
        print("END OF GENERATED OUTPUT")
        print("" + "- " * 12 + "\n")

        should_copy = input("Copy output to clipboard? [y/n]\n")

        if should_copy == "y":
            subprocess.run("pbcopy", universal_newlines=True, input=request)

    unit_test = process_test_template(
        request_name,
        request_content,
        dynamic_values,
        path_params,
        use_dynamic_values_setter,
    )

    if not is_windowed:
        print("\n" + "- " * 8)
        print("GENERATED TEST:")
        print("" + "- " * 8 + "\n")
        pprint_color(unit_test)
        print("\n" + "- " * 12)
        print("END OF GENERATED OUTPUT")
        print("" + "- " * 12 + "\n")

        if should_copy == "y":
            subprocess.run("pbcopy", universal_newlines=True, input=unit_test)

    return request, unit_test


def run_main_process(
    user_input=None,
    is_windowed=False,
    should_make_request=False,
    dynamic_values={},
    path_params={},
    use_dynamic_values_setter=False,
):
    request_name, description, request_content, response_json = parse_inputs(
        user_input, should_make_request, path_params
    )
    return process_inputs(
        request_name,
        description,
        request_content,
        response_json,
        is_windowed,
        dynamic_values,
        path_params,
        use_dynamic_values_setter,
    )
