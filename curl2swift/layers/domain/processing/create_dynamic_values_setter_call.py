from curl2swift.constants import TWO_LEVEL_INDENT_SEP
import re
from curl2swift.layers.domain.parsing.parse_content import ParsedContent
from typing import Dict
from curl2swift.layers.domain.parameter_type import ParameterType


TEMPLATE = """.setDynamicValues(
        <SETTER_CALLS>
    )"""


def create_dynamic_values_setter_call(
    parsed_content: ParsedContent,
    dynamic_values: Dict[ParameterType, str],
    path_params: Dict[str, str],
):
    function_parameter_rows = []

    for dynamic_value in dynamic_values[ParameterType.PATH_PARAM]:
        function_parameter_rows.append(
            f'{dynamic_value}PathParam: "{path_params.get(dynamic_value)}"'
        )

    for dynamic_value in dynamic_values[ParameterType.QUERY_PARAM]:
        function_parameter_rows.append(
            f'{dynamic_value}QueryParam: "{parsed_content.query_params[dynamic_value]}"'
        )

    for dynamic_value in dynamic_values[ParameterType.HEADER]:
        for row in parsed_content.header_rows:
            if dynamic_value in row:
                enum_case = re.findall("case (.*) =", row)[0]
                function_parameter_rows.append(
                    f'{enum_case}Header: "{parsed_content.headers[dynamic_value]}"'
                )

    for dynamic_value in dynamic_values[ParameterType.BODY_PARAM]:
        for index, param in enumerate(parsed_content.param_names):
            if param[0] == dynamic_value:
                enum_case = re.findall(
                    "case (.*) =", parsed_content.body_param_rows[index]
                )[0]
                function_parameter_rows.append(f'{enum_case}BodyParam: "{param[1]}"')

    if not function_parameter_rows:
        return "// Select which parameters are dynamic first."

    processed_template = TEMPLATE.replace(
        "<SETTER_CALLS>", ("," + TWO_LEVEL_INDENT_SEP).join(function_parameter_rows)
    )

    return processed_template
