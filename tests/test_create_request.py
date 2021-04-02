from curl2swift.parsing.parse_context import RequestProperties
from tests.test_request import TEST_REQUEST
from curl2swift.parsing.get_parser import get_curl_parser
from curl2swift.processing.create_request import create_request

CURL = """curl -i https://api.github.com/users/defunkt"""


def test_create_request():
    parser = get_curl_parser()
    context = RequestProperties('get', 'https://api.github.com/users/defunkt', None, None, None, None, None, ())
    request = create_request(context)
    assert request == TEST_REQUEST.strip()
