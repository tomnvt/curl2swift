from curl2swift.layers.domain.parsing.parse_content import ParsedContent
from curl2swift.layers.domain.parameter_type import ParameterType

TEST_PARSED_CONTENT = ParsedContent(
    "www.test.com",
    "GET",
    "path/{pathParam1}/{pathParam2}/",
    {"queryParam1": "queryParamValue1", "queryParam2": "queryParamValue2"},
    {"header1": "header1value", "header2": "header2value", "header3": "header3value"},
    [("bodyParam1", "bodyParam1value"), ("bodyParam2", "bodyParam2value")],
    ["pathParam1", "pathParam2"],
    ['case header1 = "header1"', 'case header2 = "header2"'],
    ['case bodyParam1 = "bodyParam1"', 'case bodyParam2 = "bodyParam2"'],
)


TEST_DYNAMIC_VALUES = {
    ParameterType.HEADER: ["header1", "header2"],
    ParameterType.QUERY_PARAM: ["queryParam1"],
    ParameterType.PATH_PARAM: ["pathParam1", "pathParam2"],
    ParameterType.BODY_PARAM: ["bodyParam1"],
}
