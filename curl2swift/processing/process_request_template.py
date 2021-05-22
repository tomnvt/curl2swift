from curl2swift.processing.prepare_enum_cases import prepare_enum_cases
import subprocess
import re

from curl2swift.processing.request_template.process_query_params import (
    process_query_params,
)
from curl2swift.parsing.parse_content import ParsedContent
from curl2swift.templates.request_templates import (
    REQUEST_TEMPLATE,
    PATH_PARAM_SETTER,
    HEADER_PARAM_SETTER,
    BODY_PARAM_SETTER,
)
from curl2swift.utils.logger import logging
from curl2swift.utils.pprint_color import pprint_color
from curl2swift.constants import TWO_LEVEL_INDENT_SEP


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
    processed_template = processed_template.replace("<PATH>", content.path)

    path_param_rows = [
        "setPathParameter(." + param_name + ', "' + path_params[param_name] + '")'
        for param_name in path_params
        if param_name not in dynamic_values["PATH PARAM"]
    ]
    if path_param_rows:
        processed_template = processed_template.replace(
            "<PATH_PARAMS_INIT>", TWO_LEVEL_INDENT_SEP.join(path_param_rows)
        )
    else:
        processed_template = processed_template.replace(
            "<PATH_PARAMS_INIT>\n        ", ""
        )

    header_rows = [
        "setHeader(." + header + ', "' + content.headers[header] + '")'
        for header in content.headers
        if header not in dynamic_values["HEADER"]
    ]
    if header_rows:
        processed_template = processed_template.replace(
            "<HEADER_PARAMS_INIT>", TWO_LEVEL_INDENT_SEP.join(header_rows)
        )
    else:
        processed_template = processed_template.replace(
            "<HEADER_PARAMS_INIT>\n        ", ""
        )

    body_param_rows = [
        "setBodyParameter(." + param[0] + ', "' + param[1] + '")'
        for param in content.param_names
        if param[0] not in dynamic_values["BODY PARAM"]
    ]
    if body_param_rows:
        processed_template = processed_template.replace(
            "<BODY_PARAMS_INIT>", TWO_LEVEL_INDENT_SEP.join(body_param_rows)
        )
    else:
        processed_template = processed_template.replace(
            "<BODY_PARAMS_INIT>\n        ", ""
        )

    processed_template = processed_template.replace(
        "<METHOD>", "." + content.method.lower()
    )

    processed_template = processed_template.replace(
        "<HEADERS>", TWO_LEVEL_INDENT_SEP.join(content.header_rows)
    )
    processed_template = processed_template.replace(
        "<BODY_PARAMS>", TWO_LEVEL_INDENT_SEP.join(content.body_param_rows)
    )

    processed_template = process_query_params(
        content.query_params, processed_template, dynamic_values
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

    processed_template = processed_template.replace("<RESPONSE>", response_model)

    return processed_template
