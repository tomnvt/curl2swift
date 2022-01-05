from curl2swift.constants import THREE_LEVEL_INDENT_SEP, TWO_LEVEL_INDENT_SEP
from curl2swift.layers.domain.processing.create_dynamic_values_setter_call import (
    create_dynamic_values_setter_call,
)
from curl2swift.layers.domain.parameter_type import ParameterType
from curl2swift.layers.domain.parsing.parse_content import ParsedContent
import re

from curl2swift.utils.logger import logging
from curl2swift.templates.test_template import TEST_TEMPLATE


def process_test_template(
    request_name,
    content: ParsedContent,
    dynamic_values,
    path_params,
    use_dynamic_values_setter,
):
    logging.info("Processing unit test templacte")
    processed_template = TEST_TEMPLATE
    processed_template = processed_template.replace("<URL>", content.url)
    if use_dynamic_values_setter:
        processed_template = _add_dynamic_params_setter_call(
            processed_template, content, dynamic_values, path_params
        )
    else:
        processed_template = _add_setter_calls(
            processed_template, content, dynamic_values, path_params
        )

    processed_template = processed_template.replace("<REQUEST_NAME>", request_name)

    return processed_template


def _get_path_param_setters(dynamic_values, path_params):
    path_param_setters = []
    for path_param in path_params:
        if path_param not in dynamic_values[ParameterType.PATH_PARAM]:
            continue
        value = path_params[path_param]
        path_param_setters.append(
            ".setPathParameter(." + path_param + ', "' + value + '")'
        )
    return path_param_setters


def _get_query_param_setters(content: ParsedContent, dynamic_values):
    query_param_setters = []
    if not content.query_params:
        return []
    for param in content.query_params:
        if param not in dynamic_values[ParameterType.QUERY_PARAM]:
            continue
        query_param_setters.append(
            ".setQueryParameter(." + param + ', "' + content.query_params[param] + '")'
        )
    return query_param_setters


def _get_header_setters(content, dynamic_values):
    header_setters = []
    for index, header in enumerate(content.headers):
        if dynamic_values and header not in dynamic_values[ParameterType.HEADER]:
            continue
        value = content.headers[header]
        enum_case = re.findall("case (.*) =", content.header_rows[index])[0]
        header_setters.append(".setHeader(." + enum_case + ', "' + value + '")')
    return header_setters


def _get_body_param_setters(content, dynamic_values):
    body_param_setters = []
    for index, param in enumerate(content.param_names):
        if (
            dynamic_values
            and content.param_names[index][0]
            not in dynamic_values[ParameterType.BODY_PARAM]
        ):
            continue
        if len(param) == 1:
            continue
        value = param[1]
        enum_case = re.findall("case (.*) =", content.body_param_rows[index])[0]
        body_param_setters.append(
            ".setBodyParameter(." + enum_case + ', "' + str(value) + '")'
        )
    return body_param_setters


def _add_dynamic_value_setters(value_rows, processed_template, placeholder):
    if value_rows:
        processed_template = processed_template.replace(
            placeholder, THREE_LEVEL_INDENT_SEP.join(value_rows)
        )
    else:
        processed_template = processed_template.replace(
            placeholder + THREE_LEVEL_INDENT_SEP, ""
        )
    return processed_template


def _add_dynamic_params_setter_call(
    processed_template, content, dynamic_values, path_params
):
    for placeholder in [
        "<PATH_PARAM_SETTERS>",
        "<QUERY_PARAM_SETTERS>",
        "<HEADER_SETTERS>",
        "<BODY_PARAM_SETTERS>",
    ]:
        processed_template = processed_template.replace(
            "            " + placeholder + "\n", ""
        )
        dynamic_values_setter_call = create_dynamic_values_setter_call(
            content, dynamic_values, path_params
        )
        dynamic_values_setter_call_rows = [
            row for row in dynamic_values_setter_call.split("\n")
        ]
        dynamic_values_setter_call = TWO_LEVEL_INDENT_SEP.join(
            dynamic_values_setter_call_rows
        )
        processed_template = processed_template.replace(
            "<DYNAMIC_VALUES_SETTER_CALL>", dynamic_values_setter_call
        )
    return processed_template


def _add_setter_calls(processed_template, content, dynamic_values, path_params):
    path_param_setters = _get_path_param_setters(dynamic_values, path_params)
    query_param_setters = _get_query_param_setters(content, dynamic_values)
    header_setters = _get_header_setters(content, dynamic_values)
    body_param_setters = _get_body_param_setters(content, dynamic_values)

    processed_template = processed_template.replace(
        "            <DYNAMIC_VALUES_SETTER_CALL>\n", ""
    )
    processed_template = _add_dynamic_value_setters(
        path_param_setters, processed_template, "<PATH_PARAM_SETTERS>"
    )
    processed_template = _add_dynamic_value_setters(
        query_param_setters, processed_template, "<QUERY_PARAM_SETTERS>"
    )
    processed_template = _add_dynamic_value_setters(
        header_setters, processed_template, "<HEADER_SETTERS>"
    )
    processed_template = _add_dynamic_value_setters(
        body_param_setters, processed_template, "<BODY_PARAM_SETTERS>"
    )

    return processed_template
