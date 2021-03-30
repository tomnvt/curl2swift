import argparse

def get_curl_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('command')
    parser.add_argument('url')
    parser.add_argument('-d', '--data')
    parser.add_argument('-b', '--data-binary', '--data-raw', default=None)
    parser.add_argument('--data-urlencode', '--data-urlencode', action='append', default=[])
    parser.add_argument('-X', default='')
    parser.add_argument('-H', '--header', action='append', default=[])
    parser.add_argument('--compressed', action='store_true')
    parser.add_argument('-k','--insecure', action='store_true')
    parser.add_argument('--user', '-u', default=())
    parser.add_argument('-i','--include', action='store_true')
    parser.add_argument('-s','--silent', action='store_true')
    parser.add_argument('--location', default=None)
    parser.add_argument('--request', default=None)
    parser.add_argument('-v', default=None)

    return parser
