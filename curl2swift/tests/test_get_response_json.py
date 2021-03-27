from curl2swift.tests.test_request import TEST_REQUEST
from curl2swift.processing.get_response_json import get_response_json


def test_get_response_json():
    json = get_response_json(TEST_REQUEST)
    assert isinstance(json, dict)
    assert json['url'] == 'https://api.github.com/users/defunkt'
