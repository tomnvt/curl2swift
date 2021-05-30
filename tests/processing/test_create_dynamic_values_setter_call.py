from tests.processing.constants import TEST_DYNAMIC_VALUES, TEST_PARSED_CONTENT
from curl2swift.layers.domain.processing.create_dynamic_values_setter_call import (
    create_dynamic_values_setter_call,
)

EXPECTED_RESULT = """
    .setDynamicValues(
        pathParam1PathParam: "pathParam1Value",
        pathParam2PathParam: "pathParam2Value",
        queryParam1QueryParam: "queryParamValue1",
        header1Header: "header1value",
        header2Header: "header2value",
        bodyParam1BodyParam: "bodyParam1value"
    )
"""

TEST_PATH_PARAMS = {"pathParam1": "pathParam1Value", "pathParam2": "pathParam2Value"}


def test_create_dynamic_values_setter():
    result = create_dynamic_values_setter_call(
        TEST_PARSED_CONTENT, TEST_DYNAMIC_VALUES, TEST_PATH_PARAMS
    )
    assert result.strip() == EXPECTED_RESULT.strip()
