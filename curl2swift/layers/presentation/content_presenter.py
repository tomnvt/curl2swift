from curl2swift.parsing.get_parser import get_curl_parser
from curl2swift.parsing.parse_content import ParsedContent, get_request_content
from curl2swift.run_main_process import run_main_process

from collections import namedtuple
from dataclasses import dataclass

@dataclass
class WindowViewModel:
    request_content: ParsedContent
    request_tab_text: str
    unit_test_tab_text: str
    dynamic_values: dict


class ContentPresenter:

    user_input = None
    dynamic_values = {'HEADER': [], 'QUERY PARAM': [], 'BODY PARAM': []}

    def __init__(self, on_change):
        self.on_change = on_change

    def on_input_changed(self, user_input):
        # TODO: Handle selected dynamic values migration
        self.user_input = user_input
        request, unit_test = run_main_process(user_input, True)
        self.update(user_input, request, unit_test, self.dynamic_values)

    def on_go_button_click(self):
        if self.user_input:
            request, unit_test = run_main_process(self.user_input, True, True)
            self.update(self.user_input, request, unit_test)

    def update(self, user_input, request, unit_test, dynamic_values):
        parser = get_curl_parser()
        content, _ = get_request_content(parser, user_input.curl)
        view_model = WindowViewModel(content, request, unit_test, self.dynamic_values)
        self.on_change(view_model)

    def on_dynamic_parameter_selection_change(self, selected):
        dynamic_values = {'HEADER': [], 'QUERY PARAM': [], 'BODY PARAM': []}
        for selected_pair in selected:
            split = selected_pair.split(' - ')
            dynamic_values[split[0]].append(split[1])
        self.dynamic_values = dynamic_values
        request, unit_test = run_main_process(self.user_input, True, False, dynamic_values)
        self.update(self.user_input, request, unit_test, dynamic_values)

