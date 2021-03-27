from curl2swift.tests.test_request import TEST_REQUEST
from curl2swift.processing.get_response_json import get_response_json

RESPONSE_JSON = {
    'avatar_url': 'https://avatars.githubusercontent.com/u/2?v=4',
    'bio': '🍔',
    'blog': 'http://chriswanstrath.com/',
    'company': None,
    'created_at': '2007-10-20T05:24:19Z',
    'email': None,
    'events_url': 'https://api.github.com/users/defunkt/events{/privacy}',
    'followers': 21166,
    'followers_url': 'https://api.github.com/users/defunkt/followers',
    'following': 210,
    'following_url': 'https://api.github.com/users/defunkt/following{/other_user}',
    'gists_url': 'https://api.github.com/users/defunkt/gists{/gist_id}',
    'gravatar_id': '',
    'hireable': None,
    'html_url': 'https://github.com/defunkt',
    'id': 2,
    'location': None,
    'login': 'defunkt',
    'name': 'Chris Wanstrath',
    'node_id': 'MDQ6VXNlcjI=',
    'organizations_url': 'https://api.github.com/users/defunkt/orgs',
    'public_gists': 273,
    'public_repos': 107,
    'received_events_url': 'https://api.github.com/users/defunkt/received_events',
    'repos_url': 'https://api.github.com/users/defunkt/repos',
    'site_admin': False,
    'starred_url': 'https://api.github.com/users/defunkt/starred{/owner}{/repo}',
    'subscriptions_url': 'https://api.github.com/users/defunkt/subscriptions',
    'twitter_username': None,
    'type': 'User',
    'updated_at': '2019-11-01T21:56:00Z',
    'url': 'https://api.github.com/users/defunkt'
}


def test_get_response_json():
    json = get_response_json(TEST_REQUEST)
    assert json == RESPONSE_JSON
