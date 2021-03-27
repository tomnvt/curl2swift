from curl2swift.create_request import create_request
from curl2swift.get_parser import get_parser

curl = """curl -i https://api.github.com/users/defunkt"""

expected_request_code = """
requests.get("https://api.github.com/users/defunkt",
    headers={},
    cookies={},
    auth=(),
)
""".strip()

def test_create_request():
    parser = get_parser()
    request = create_request(curl, parser)
    assert request == expected_request_code
