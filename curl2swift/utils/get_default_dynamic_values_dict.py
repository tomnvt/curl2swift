from typing import Dict, List
from curl2swift.layers.domain.parameter_type import ParameterType


def get_default_dynamic_values_dict() -> Dict[ParameterType, List[str]]:
    return {
        ParameterType.HEADER: [],
        ParameterType.QUERY_PARAM: [],
        ParameterType.BODY_PARAM: [],
        ParameterType.PATH_PARAM: [],
    }
