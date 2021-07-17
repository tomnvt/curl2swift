from curl2swift.utils.get_default_dynamic_values_dict import (
    get_default_dynamic_values_dict,
)
from curl2swift.layers.domain.parameter_type import ParameterType
from curl2swift.layers.domain.parsing.get_parser import get_curl_parser
from curl2swift.layers.domain.parsing.parse_content import (
    ParsedContent,
    get_request_content,
)
from curl2swift.generate_output import generate_ouput

from dataclasses import dataclass


@dataclass
class ViewModel:
    request_content: ParsedContent
    request_tab_text: str
    unit_test_tab_text: str
    dynamic_values: dict


class ContentPresenter:

    # --- Properties ---
    _user_input = None
    _use_dynamic_values_setter = False
    dynamic_values = get_default_dynamic_values_dict()
    path_parameters_dictionary = {}

    # --- Init ---
    def __init__(self, on_change, on_dynamic_values_change):
        self.on_change = on_change
        self.on_dynamic_values_change = on_dynamic_values_change

    # --- Intearaction handling ---
    def on_input_changed(self, user_input):
        self._user_input = user_input
        self._update(update_dynamic_values=True)

    def on_go_button_click(self):
        self._update(make_request=True)

    def on_dynamic_parameter_selection_change(self, selected):
        dynamic_values = get_default_dynamic_values_dict()
        for selected_pair in selected:
            split = selected_pair.split(" - ")
            enum_case = ParameterType(split[0])
            dynamic_values[enum_case].append(split[1])
        self.dynamic_values = dynamic_values
        self._update()

    def on_path_param_line_edit_change(self, params: dict):
        if params != self.path_parameters_dictionary:
            self.path_parameters_dictionary = params
        self._update(update_dynamic_values=False)

    def test_with_dynamic_values_setter_checkbox_change(self, checked):
        self._use_dynamic_values_setter = checked
        self._update()

    # --- Private ---
    def _update(
        self,
        make_request=False,
        update_dynamic_values=False,
    ):
        if not self._user_input or not self._user_input.curl:
            return
        content, _ = get_request_content(
            self._user_input.curl, False, self.path_parameters_dictionary
        )

        dynamic_values = get_default_dynamic_values_dict()
        for header in self.dynamic_values[ParameterType.HEADER]:
            if not content.headers:
                continue
            if header in content.headers:
                dynamic_values[ParameterType.HEADER].append(header)
        for param in self.dynamic_values[ParameterType.QUERY_PARAM]:
            if not content.query_params:
                continue
            if param in content.query_params:
                dynamic_values[ParameterType.QUERY_PARAM].append(param)
        for body_param in self.dynamic_values[ParameterType.BODY_PARAM]:
            if not content.param_names:
                continue
            if body_param in [pair[0] for pair in content.param_names]:
                dynamic_values[ParameterType.BODY_PARAM].append(body_param)
        for param in self.dynamic_values[ParameterType.PATH_PARAM]:
            if not content.path_params:
                continue
            if param in content.path_params:
                dynamic_values[ParameterType.PATH_PARAM].append(param)

        self.dynamic_values = dynamic_values

        request, unit_test, _ = generate_ouput(
            user_input=self._user_input,
            is_windowed=True,
            should_make_request=make_request,
            dynamic_values=self.dynamic_values,
            path_params=self.path_parameters_dictionary,
            use_dynamic_values_setter=self._use_dynamic_values_setter,
        )
        view_model = ViewModel(content, request, unit_test, self.dynamic_values)
        self.on_change(view_model)
        if update_dynamic_values:
            self.on_dynamic_values_change(view_model)
