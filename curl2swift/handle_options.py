import getopt
import sys
import subprocess
import webbrowser

from curl2swift.utils.clone_repo import clone_repo


def open_create_issue_page():
    webbrowser.open("https://github.com/tomnvt/curl2swift/issues/new")


def clone_example_project():
    clone_repo("https://github.com/tomnvt/curl2swift-example.git", "example project")
    subprocess.Popen(["open", "curl2swift-example", "-a", "Xcode"])


def clone_boilerplate_code():
    clone_repo(
        "https://github.com/tomnvt/curl2swift-boilerplate.git",
        "boilerplate code",
    )


option_handlers = {
    **dict.fromkeys(["-i", "--issue"], open_create_issue_page),
    **dict.fromkeys(["-e", "--example"], clone_example_project),
    **dict.fromkeys(["-b", "--boilerplate"], clone_boilerplate_code),
}


def handle_options():
    options, _ = getopt.getopt(
        sys.argv[1:], "iebw", ["issue", "example", "boilerplate", "windowed", "curl="]
    )

    for opt, _ in options:
        option_handler = option_handlers.get(opt)
        if option_handler:
            option_handler()
            sys.exit(0)
