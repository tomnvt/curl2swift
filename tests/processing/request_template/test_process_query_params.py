from curl2swift.layers.domain.parameter_type import ParameterType
from curl2swift.processing.request_template.process_query_params import (
    process_query_params,
)


def test_process_query_params():
    params = {"q": "prague", "appid": "theAppID", "units": "metric"}
    result = process_query_params(params, "<QUERY_PARAMS_INIT>", {ParameterType.QUERY_PARAM: []})
    assert (
        result
        == 'set(.queryParams(["q": "prague", "appid": "theAppID", "units": "metric"]))'
    )
