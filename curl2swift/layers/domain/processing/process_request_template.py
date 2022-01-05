from curl2swift.layers.domain.processing.create_dynamic_values_setter import (
    create_dynamic_values_setter,
)
from curl2swift.layers.domain.parameter_type import ParameterType
import re

from curl2swift.layers.domain.processing.process_query_params import (
    process_query_params,
)
from curl2swift.layers.domain.parsing.parse_content import ParsedContent
from curl2swift.templates.request_templates import (
    REQUEST_TEMPLATE,
    PATH_PARAM_SETTER,
    HEADER_PARAM_SETTER,
    BODY_PARAM_SETTER,
)
from curl2swift.utils.logger import logging
from curl2swift.constants import THREE_LEVEL_INDENT_SEP, TWO_LEVEL_INDENT_SEP


def process_request_template(
    request_name,
    description,
    content: ParsedContent,
    response_model,
    dynamic_values,
    path_params,
):
    logging.info("Processing request template")
    processed_template = REQUEST_TEMPLATE
    processed_template = processed_template.replace("<REQUEST_NAME>", request_name)
    processed_template = processed_template.replace("<DESC>", description)
    processed_template = processed_template.replace("<URL>", content.url)
    processed_template = processed_template.replace("<PATH>", content.path)

    processed_template = _process_path_params(
        processed_template, content, path_params, dynamic_values
    )
    processed_template = _process_headers(processed_template, content, dynamic_values)
    processed_template = _process_body_params(
        processed_template, content, dynamic_values
    )

    processed_template = processed_template.replace(
        "<METHOD>", "." + content.method.lower()
    )

    processed_template = process_query_params(
        content.query_params, processed_template, dynamic_values
    )

    processed_template = processed_template.replace("<RESPONSE>", response_model)

    processed_template = _handle_dynamic_values_setter(
        processed_template, dynamic_values, content
    )

    return processed_template


def _process_path_params(processed_template, content, path_params, dynamic_values):
    path_param_rows = [
        "setPathParameter(." + param_name + ', "' + path_params[param_name] + '")'
        for param_name in path_params
        if param_name not in dynamic_values[ParameterType.PATH_PARAM]
    ]
    if path_param_rows:
        processed_template = processed_template.replace(
            "<PATH_PARAMS_INIT>", TWO_LEVEL_INDENT_SEP.join(path_param_rows)
        )
    else:
        processed_template = processed_template.replace(
            "<PATH_PARAMS_INIT>" + TWO_LEVEL_INDENT_SEP, ""
        )

    processed_template = processed_template.replace(
        "<PATH_PARAMS>",
        TWO_LEVEL_INDENT_SEP.join(["case " + param for param in content.path_params]),
    )
    if content.path_params:
        processed_template = processed_template.replace(
            "<PATH_PARAM_SETTER>", PATH_PARAM_SETTER
        )
    else:
        processed_template = re.sub(
            r"\n\s*enum PathParameter: String \{\n\s*\}",
            "",
            processed_template,
        )
        processed_template = re.sub("\n\s*<PATH_PARAM_SETTER>", "", processed_template)

    return processed_template


def _process_headers(processed_template, content, dynamic_values):
    header_rows = []
    for row, header in zip(content.header_rows, content.headers):
        enum_case = re.findall("case (.*) =", row)[0]
        if header not in dynamic_values[ParameterType.HEADER]:
            header_rows.append(
                "setHeader(." + enum_case + ', "' + content.headers[header] + '")'
            )

    if header_rows:
        processed_template = processed_template.replace(
            "<HEADER_PARAMS_INIT>", TWO_LEVEL_INDENT_SEP.join(header_rows)
        )
    else:
        processed_template = processed_template.replace(
            f"<HEADER_PARAMS_INIT>{TWO_LEVEL_INDENT_SEP}", ""
        )

    processed_template = processed_template.replace(
        "<HEADERS>", TWO_LEVEL_INDENT_SEP.join(content.header_rows)
    )
    if content.headers:
        processed_template = processed_template.replace(
            "<HEADER_PARAM_SETTER>", HEADER_PARAM_SETTER
        )
    else:
        processed_template = re.sub(
            r"\n\s*enum Header: String \{\n\s*\}", "", processed_template
        )
        processed_template = re.sub(
            r"\n\s*<HEADER_PARAM_SETTER>", "", processed_template
        )

    return processed_template


def _process_body_params(processed_template, content, dynamic_values):
    body_param_rows = []
    for row, param_pair in zip(content.body_param_rows, content.param_names):
        enum_case = re.findall("case (.*) =", row)[0]
        if param_pair[0] not in dynamic_values[ParameterType.BODY_PARAM]:
            body_param_rows.append(
                "setBodyParameter(." + enum_case + ', "' + str(param_pair[1]) + '")'
            )

    if body_param_rows:
        processed_template = processed_template.replace(
            "<BODY_PARAMS_INIT>", TWO_LEVEL_INDENT_SEP.join(body_param_rows)
        )
    else:
        processed_template = processed_template.replace(
            f"<BODY_PARAMS_INIT>{TWO_LEVEL_INDENT_SEP}", ""
        )

    processed_template = processed_template.replace(
        "<BODY_PARAMS>", TWO_LEVEL_INDENT_SEP.join(content.body_param_rows)
    )

    if content.param_names:
        processed_template = processed_template.replace(
            "<BODY_PARAM_SETTER>", BODY_PARAM_SETTER
        )
    else:
        processed_template = re.sub(
            r"\n\s*enum BodyParameter: String \{\n\s*\}",
            "",
            processed_template,
        )
        processed_template = re.sub("\n\s*<BODY_PARAM_SETTER>", "", processed_template)

    return processed_template


def _handle_dynamic_values_setter(processed_template, dynamic_values, content):
    if (
        dynamic_values[ParameterType.PATH_PARAM]
        or dynamic_values[ParameterType.QUERY_PARAM]
        or dynamic_values[ParameterType.HEADER]
        or dynamic_values[ParameterType.BODY_PARAM]
    ):
        dynamic_values_setters = create_dynamic_values_setter(content, dynamic_values)
        processed_template = processed_template.replace(
            "<DYNAMIC_VALUES_SETTER>", dynamic_values_setters
        )
    else:
        processed_template = processed_template.replace(
            "    <DYNAMIC_VALUES_SETTER>\n", ""
        )
    return processed_template
