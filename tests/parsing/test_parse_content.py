import sys

import curl2swift.parsing.parse_content as test_class

TEST_CURL = 'curl https://api.openweathermap.org/data/2.5/weather?q=hronov&appid=KEY&units=metric'


def test_get_curl_from_arguments():
    sys.argv = ['some', 'more', 'random', '--curl', TEST_CURL, 'other', 'args']
    curl = test_class.get_curl()
    assert curl == TEST_CURL
