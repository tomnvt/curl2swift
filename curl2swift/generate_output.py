from curl2swift.utils.get_default_dynamic_values_dict import (
    get_default_dynamic_values_dict,
)
from curl2swift.layers.domain.parameter_type import ParameterType
from curl2swift.utils.pprint_color import pprint_color
import subprocess
from curl2swift.layers.domain.parsing.get_parser import get_curl_parser
from curl2swift.layers.domain.parsing.parse_content import get_request_content
from curl2swift.layers.domain.parsing.get_request_name_and_description import (
    get_request_name_and_description,
)
from curl2swift.layers.domain.processing.create_response_model import (
    create_response_model,
)
from curl2swift.layers.domain.processing.process_test_template import (
    process_test_template,
)
from curl2swift.layers.domain.processing.process_request_template import (
    process_request_template,
)

cached_response = {}


def _parse_inputs(user_input, should_make_request=False, path_params={}):
    global cached_response
    parser = get_curl_parser()
    if user_input:
        request_name, description = user_input.request_name, user_input.description
    else:
        request_name, description = get_request_name_and_description()
    request_content, response_json = get_request_content(
        user_input.curl if user_input else None,
        should_make_request,
        path_params,
    )
    if should_make_request:
        cached_response = response_json
    else:
        response_json = cached_response
    return request_name, description, request_content, response_json


def _show_output(output, output_type):
    print("\n" + "- " * 9)
    print(f"GENERATED {output_type}:")
    print("" + "- " * 9 + "\n")
    pprint_color(output)
    print("\n" + "- " * 12)
    print("END OF GENERATED OUTPUT")
    print("" + "- " * 12 + "\n")

    should_copy = input("Copy output to clipboard? [y/n]\n")

    if should_copy == "y":
        subprocess.run("pbcopy", universal_newlines=True, input=output)


def _process_inputs(
    request_name,
    description,
    request_content,
    response_json,
    is_windowed,
    dynamic_values,
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
        _show_output(request, "REQUEST")

    unit_test = process_test_template(
        request_name,
        request_content,
        dynamic_values,
        path_params,
        use_dynamic_values_setter,
    )

    if not is_windowed:
        _show_output(unit_test, "TEST")

    return request, unit_test, response_json


def generate_ouput(
    user_input=None,
    is_windowed=False,
    should_make_request=False,
    dynamic_values=get_default_dynamic_values_dict(),
    path_params={},
    use_dynamic_values_setter=False,
):
    request_name, description, request_content, response_json = _parse_inputs(
        user_input, should_make_request, path_params
    )
    return _process_inputs(
        request_name,
        description,
        request_content,
        response_json,
        is_windowed,
        dynamic_values,
        path_params,
        use_dynamic_values_setter,
    )
