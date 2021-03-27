from curl2swift.tests.test_request import TEST_REQUEST
from curl2swift.get_response_json import get_response_json

def test_get_response_json():
    json = get_response_json(TEST_REQUEST)
