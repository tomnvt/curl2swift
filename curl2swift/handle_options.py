import getopt
import sys
import subprocess
import webbrowser

from curl2swift.utils.clone_repo import clone_repo

def handle_options():
    options, arguments = getopt.getopt(
        sys.argv[1:],
        "ieb",
        ["issue", "example", 'boilerplate', 'curl=']
    )

    for opt, value in options:
        if opt in ["-i", '--issue']:
            webbrowser.open('https://github.com/tomnvt/curl2swift/issues/new')
            sys.exit(0)
        if opt in ["-e", "--example"]:
            clone_repo('https://github.com/tomnvt/curl2swift-example.git', 'example project')
            subprocess.Popen(['open', 'curl2swift-example', '-a', 'Xcode'])
            sys.exit(0)
        if opt in ["-b", "--boilerplate"]:
            clone_repo('https://github.com/tomnvt/curl2swift-boilerplate.git', 'boilerplate code')
            sys.exit(0)
        if opt in ["-c", "--curl"]:
            return {'curl': value}
