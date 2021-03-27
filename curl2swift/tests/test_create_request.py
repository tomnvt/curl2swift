from curl2swift.tests.test_request import TEST_REQUEST
from curl2swift.parsing.get_parser import get_curl_parser
from curl2swift.processing.create_request import create_request

CURL = """curl -i https://api.github.com/users/defunkt"""


def test_create_request():
    parser = get_curl_parser()
    request = create_request(CURL, parser)
    assert request == TEST_REQUEST.strip()
