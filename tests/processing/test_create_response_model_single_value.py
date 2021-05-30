from ast import literal_eval
from curl2swift.layers.domain.processing.create_response_model import (
    create_response_model,
)

RESPONSE = "12345"

EXPECTED_RESULT = """
    typealias Response = Int
"""


def test_create_response_model():
    json_dict = literal_eval(RESPONSE)
    response_model = create_response_model(json_dict)
    assert response_model.strip() == EXPECTED_RESULT.strip()
