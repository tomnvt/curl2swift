from enum import Enum


class ParameterType(Enum):
    HEADER = "HEADER"
    QUERY_PARAM = "QUERY PARAM"
    BODY_PARAM = "BODY PARAM"
    PATH_PARAM = "PATH PARAM"
