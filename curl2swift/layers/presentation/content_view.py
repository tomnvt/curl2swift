from curl2swift.layers.presentation.swift_highlighter import SwiftHighlighter
from curl2swift.layers.presentation.curl_highlighter import CurlHighlighter
from PyQt5 import QtCore
from curl2swift.layers.presentation.dynamic_parameters_selector_view import (
    DynamicParamsSelectorView,
)
from curl2swift.__main__ import main

from curl2swift.layers.presentation.content_presenter import (
    ContentPresenter,
    ViewModel,
)
from typing import NamedTuple

from PyQt5.QtWidgets import (
    QCheckBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QSplitter,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

EXAMPLE_CURL = """
curl --location --request POST 'https://www.host.com/path/{pathParam}/morePath?queryParam=value' \\
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

    # --- Properties ---
    info_labels = []

    @property
    def user_input(self):
        request_name = self.request_name_input.text()
        description = self.description_input.text()
        curl = self.curl_text_edit.toPlainText()
        return UserInput(request_name, description, curl)

    # --- Init ---
    def __init__(self, screen_width):
        super().__init__()
        self.presenter = ContentPresenter(
            self.on_output_change, self.on_dynamic_values_change
        )
        self.selector = DynamicParamsSelectorView(self.presenter)
        self._layout_views()
        self._bind_interactions()
        self.curl_text_edit.setPlainText(EXAMPLE_CURL)

    # --- Setup ---
    def _layout_views(self):
        layout = QHBoxLayout()
        self.splitter = QSplitter()
        layout.addWidget(self.splitter)

        self._setup_input_part()
        self._setup_output_part()

        self.setLayout(layout)

        self.left_half_layout.addWidget(self.selector)

    def _setup_input_part(self):
        self.request_name_input = QLineEdit()
        self.request_name_input.setText("Example")
        self.request_name_input.setMinimumWidth(200)
        self.description_input = QLineEdit()
        self.description_input.setMinimumWidth(200)
        self.curl_text_edit = QPlainTextEdit()
        self.highlight = CurlHighlighter(self.curl_text_edit.document())
        self.description_input.setText("Add description")
        self.curl_label = QLabel("cURL:")
        self.left_half_frame = QFrame()
        self.left_half_layout = QVBoxLayout()
        self.left_half_frame.setLayout(self.left_half_layout)

        form_layout = QFormLayout()
        form_layout.addRow("Request name: ", self.request_name_input)
        form_layout.addRow("Description: ", self.description_input)
        form_layout.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        form_layout.setContentsMargins(0, 10, 0, 10)

        self.left_half_layout.addLayout(form_layout)
        self.left_half_layout.addWidget(self.curl_label)
        self.left_half_layout.addWidget(self.curl_text_edit)
        self.splitter.addWidget(self.left_half_frame)

    def _setup_output_part(self):
        self.go_button = QPushButton("MAKE REQUEST AND CREATE RESPONSE MAPPING")
        self.test_with_dynamic_values_setter_checkbox = QCheckBox(
            "Use dynamic values setter"
        )
        self.test_with_dynamic_values_setter_checkbox.stateChanged.connect(
            self.presenter.test_with_dynamic_values_setter_checkbox_change
        )
        self.right_half_frame = QFrame()
        self.right_half_layout = QVBoxLayout()
        self.right_half_frame.setLayout(self.right_half_layout)
        self.tabs = self._get_tabs()
        self.right_half_layout.addWidget(self.tabs)
        self.splitter.addWidget(self.right_half_frame)

    def _get_tabs(self):
        tabs = QTabWidget()
        self.request_text_edit = SwiftHighlighter()
        self.unit_test_text_edit = SwiftHighlighter()
        tabs.addTab(
            self._create_tab([self.request_text_edit, self.go_button]),
            "RequestSpecBuilder",
        )
        tabs.addTab(
            self._create_tab(
                [
                    self.unit_test_text_edit,
                    self.test_with_dynamic_values_setter_checkbox,
                ]
            ),
            "Unit test",
        )
        return tabs

    def _create_tab(self, widgets):
        tab_widget = QWidget()
        layout = QVBoxLayout()
        for widget in widgets:
            layout.addWidget(widget)
        tab_widget.setLayout(layout)
        return tab_widget

    # --- Interaction binding ---
    def _bind_interactions(self):
        self.request_name_input.textChanged.connect(self._on_input_change)
        self.description_input.textChanged.connect(self._on_input_change)
        self.curl_text_edit.textChanged.connect(self._on_input_change)
        self.go_button.clicked.connect(self._on_go_button_click)

    def _on_input_change(self):
        self.presenter.on_input_changed(self.user_input)

    def _on_go_button_click(self):
        self.presenter.on_go_button_click()

    # --- Data binding ---
    def on_output_change(self, view_model: ViewModel):
        scroll_position = self.unit_test_text_edit.verticalScrollBar().value()
        self.unit_test_text_edit.setText(view_model.unit_test_tab_text)
        self.unit_test_text_edit.verticalScrollBar().setValue(scroll_position)

        scroll_position = self.request_text_edit.verticalScrollBar().value()
        self.request_text_edit.setText(view_model.request_tab_text)
        self.request_text_edit.verticalScrollBar().setValue(scroll_position)

    def on_dynamic_values_change(self, view_model: ViewModel):
        self.selector.update(view_model)
