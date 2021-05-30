from tests.processing.constants import TEST_DYNAMIC_VALUES, TEST_PARSED_CONTENT
from curl2swift.layers.domain.processing.create_dynamic_values_setter import (
    create_dynamic_values_setter,
)


EXPECTED_RESULT = """
    @discardableResult
    func setDynamicValues(
        pathParam1PathParam: String,
        pathParam2PathParam: String,
        queryParam1QueryParam: String,
        header1Header: String,
        header2Header: String,
        bodyParam1BodyParam: Any
    ) -> Self {
        setPathParameter(.pathParam1, pathParam1PathParam)
        setPathParameter(.pathParam2, pathParam2PathParam)
        setQueryParam(.queryParam1, queryParam1QueryParam)
        setHeader(.header1, header1Header)
        setHeader(.header2, header2Header)
        setBodyParam(.bodyParam1, bodyParam1BodyParam)
        return self
    }
"""


def test_create_dynamic_values_setter():
    result = create_dynamic_values_setter(TEST_PARSED_CONTENT, TEST_DYNAMIC_VALUES)
    print(EXPECTED_RESULT)
    print()
    print(result)
    assert result.strip() == EXPECTED_RESULT.strip()
