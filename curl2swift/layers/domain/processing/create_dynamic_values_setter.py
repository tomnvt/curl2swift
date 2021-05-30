from curl2swift.constants import TWO_LEVEL_INDENT_SEP
import re
from curl2swift.layers.domain.parsing.parse_content import ParsedContent
from typing import Dict
from curl2swift.layers.domain.parameter_type import ParameterType


TEMPLATE = """
    @discardableResult
    func setDynamicValues(
        <PARAMETERS>
    ) -> Self {
        <SETTERS>
        return self
    }
"""


def create_dynamic_values_setter(
    parsed_content: ParsedContent,
    dynamic_values: Dict[ParameterType, str],
):
    function_parameter_rows = []
    assignment_rows = []

    for dynamic_value in dynamic_values[ParameterType.PATH_PARAM]:
        function_parameter_rows.append(f"{dynamic_value}PathParam: String")
        assignment_rows.append(
            f"setPathParameter(.{dynamic_value}, {dynamic_value}PathParam)"
        )

    for dynamic_value in dynamic_values[ParameterType.QUERY_PARAM]:
        function_parameter_rows.append(f"{dynamic_value}QueryParam: String")
        assignment_rows.append(
            f"setQueryParam(.{dynamic_value}, {dynamic_value}QueryParam)"
        )

    for dynamic_value in dynamic_values[ParameterType.HEADER]:
        for row in parsed_content.header_rows:
            if dynamic_value in row:
                enum_case = re.findall("case (.*) =", row)[0]
                function_parameter_rows.append(f"{enum_case}Header: String")
                assignment_rows.append(f"setHeader(.{enum_case}, {enum_case}Header)")

    for dynamic_value in dynamic_values[ParameterType.BODY_PARAM]:
        for row in parsed_content.body_param_rows:
            if dynamic_value in row:
                enum_case = re.findall("case (.*) =", row)[0]
                function_parameter_rows.append(f"{enum_case}BodyParam: Any")
                assignment_rows.append(
                    f"setBodyParameter(.{enum_case}, {enum_case}BodyParam)"
                )

    processed_template = TEMPLATE.replace(
        "<PARAMETERS>", ("," + TWO_LEVEL_INDENT_SEP).join(function_parameter_rows)
    )
    processed_template = processed_template.replace(
        "<SETTERS>", TWO_LEVEL_INDENT_SEP.join(assignment_rows)
    )

    return processed_template
