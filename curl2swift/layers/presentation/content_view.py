from curl2swift.layers.presentation.dynamic_parameters_selector_view import DynamicParamsSelectorView
from curl2swift.__main__ import main

from curl2swift.layers.presentation.content_presenter import (
    ContentPresenter,
    WindowViewModel,
)
from typing import NamedTuple

from PyQt5.QtWidgets import (
    QFormLayout,
    QFrame,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

EXAMPLE_CURL = """
curl --location --request POST 'https://www.host.com/path/morePath?queryParam=value' \\
--header 'Accept-Encoding: gzip;q=1.0, compress;q=0.5' \\
--header 'Accept-Language: en;q=1.0, cs-CZ;q=0.9' \\
--header 'Content-Type: application/x-www-form-urlencoded' \\
--header 'Authorization: Bearer TOKEN' \\
--data-urlencode 'key_1=value_1' \\
--data-urlencode 'key_2=value_2'
""".strip()


class UserInput(NamedTuple):
    request_name: str
    description: str
    curl: str


class ContentView(QWidget):
    @property
    def user_input(self):
        request_name = self.request_name_input.text()
        description = self.description_input.text()
        curl = self.curl_text_edit.toPlainText()
        return UserInput(request_name, description, curl)

    def on_input_change(self):
        self.presenter.on_input_changed(self.user_input)

    def on_go_button_click(self):
        self.presenter.on_go_button_click()

    info_labels = []

    def on_change(self, view_model: WindowViewModel):
        self.unit_test_text_edit.setText(view_model.unit_test_tab_text)
        self.request_text_edit.setText(view_model.request_tab_text)
        self._set_dynamic_params_selector(view_model)


    def _set_dynamic_params_selector(self, view_model):
        self.selector.update(view_model)


    def __init__(self, screen_width):
        super().__init__()
        self.presenter = ContentPresenter(self.on_change)
        self.selector = DynamicParamsSelectorView(self.presenter)

        """ Widgets """
        # cURL input field
        self.request_name_input = QLineEdit()
        self.description_input = QLineEdit()
        self.curl_text_edit = QPlainTextEdit()
        self.description_input.setText("Add description")
        self.curl_label = QLabel("cURL:")

        # Info label
        self.info_label = QWidget()
        self.go_button = QPushButton("MAKE REQUEST AND CREATE RESPONSE MAPPING")

        self.setWindowTitle("curl2swift")

        """ Layout """
        layout = QGridLayout()

        # Left half
        self.left_half_frame = QFrame()
        self.left_half_layout = QVBoxLayout()
        self.left_half_frame.setLayout(self.left_half_layout)
        form_layout = QFormLayout()
        form_layout.addRow("Request name: ", self.request_name_input)
        form_layout.addRow("Description: ", self.description_input)
        self.left_half_layout.addLayout(form_layout)
        self.left_half_layout.addWidget(self.curl_label)
        self.left_half_layout.addWidget(self.curl_text_edit)

        self.templates_view = self.get_templates_tabs(screen_width)

        layout.addWidget(self.left_half_frame, 0, 0)
        layout.addWidget(self.templates_view, 0, 0)

        # Right half
        tabs = self.get_tabs(screen_width)
        layout.addWidget(tabs, 0, 1)

        # Overlay
        self.setLayout(layout)
        self.templates_view.hide()

        self.request_name_input.textChanged.connect(self.on_input_change)
        self.description_input.textChanged.connect(self.on_input_change)
        self.curl_text_edit.textChanged.connect(self.on_input_change)
        self.go_button.clicked.connect(self.on_go_button_click)

        self.request_name_input.setText("Example")

        self.left_half_layout.addWidget(self.selector)
        self.curl_text_edit.setPlainText(EXAMPLE_CURL)

    def get_tabs(self, screen_width):
        tabs = QTabWidget()
        self.request_text_edit = QTextEdit()
        self.unit_test_text_edit = QTextEdit()
        self.request_call_text_edit = QTextEdit()
        tabs.addTab(
            self.create_tab([self.request_text_edit, self.go_button]), "Request"
        )
        tabs.addTab(self.create_tab([self.unit_test_text_edit]), "Unit test")
        tabs.addTab(self.create_tab([self.request_call_text_edit]), "Request call")
        return tabs

    def get_templates_tabs(self, screen_width):
        tabs = QTabWidget()
        self.request_template_text_edit = QTextEdit()
        self.unit_test_template_text_edit = QTextEdit()
        tabs.addTab(self.create_tab([self.request_template_text_edit]), "RequestSpecBuilder")
        tabs.addTab(self.create_tab([self.unit_test_template_text_edit]), "Unit test")
        return tabs

    def create_tab(self, widgets):
        tab_widget = QWidget()
        layout = QVBoxLayout()
        for widget in widgets:
            layout.addWidget(widget)
        tab_widget.setLayout(layout)
        return tab_widget
