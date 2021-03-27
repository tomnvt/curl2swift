from curl2swift.get_response_json import get_response_json

request_code = """
requests.get("https://api.github.com/users/defunkt",
    headers={},
    cookies={},
    auth=(),
)
""".strip()

def test_get_response_json():
    json = get_response_json(request_code)
