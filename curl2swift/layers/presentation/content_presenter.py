from curl2swift.parsing.get_parser import get_curl_parser
from curl2swift.parsing.parse_content import get_request_content
from curl2swift.run_main_process import run_main_process

from collections import namedtuple

WindowViewModel = namedtuple(
    "WindowViewModel", ["info_label_text", "request_tab_text", "unit_test_tab_text"]
)


class ContentPresenter:
    def __init__(self, on_change):
        self.on_change = on_change

    def on_input_changed(self, user_input):
        request, unit_test = run_main_process(user_input, True)
        self.update(user_input, request, unit_test)

    def on_go_button_click(self, user_input):
        request, unit_test = run_main_process(user_input, True, True)
        self.update(user_input, request, unit_test)

    def update(self, user_input, request, unit_test):
        parser = get_curl_parser()
        content, _ = get_request_content(parser, user_input.curl)
        content_print = (
            "BASE URL: "
            + content.url
            + "\n"
            + "PATH: "
            + content.path
            + "\n"
            + "PATH PARAMS: "
            + str(content.path_param_rows)
            + "\n"
            + "HEADERS: "
            + str(content.headers)
            + "\n"
            + "BODY PARAMS: "
            + str(content.body_param_rows)
            + "\n"
        )
        view_model = WindowViewModel(content_print, request, unit_test)
        self.on_change(view_model)
