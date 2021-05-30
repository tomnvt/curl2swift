from curl2swift.layers.domain.parameter_type import ParameterType
from PyQt5 import QtCore
from curl2swift.layers.presentation.content_presenter import (
    ContentPresenter,
    ViewModel,
)
from PyQt5.QtWidgets import (
    QCheckBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)


class DynamicParamsSelectorView(QWidget):

    """ Properties """

    _selected = set()
    _path_param_lines = []
    _check_boxes = []

    """ Init """

    def __init__(self, presenter: ContentPresenter):
        super().__init__()
        self.presenter = presenter
        self.box_layout = QVBoxLayout()
        self.info_label = QWidget()
        self.info_layout = QVBoxLayout()
        self.path_param_values_label = QLabel("Path parameters:")
        self.form_widget = QWidget()
        self.setLayout(self.box_layout)

    """ Public """

    def update(self, view_model: ViewModel):
        self._check_boxes = []
        self._path_param_lines = []
        self._reset_layout()
        self._reset_input_form()

        self._setup_path_params_input_view(view_model)
        self.info_layout.addWidget(QLabel("Which values are dynamic?"))
        self._setup_path_params_checkboxes(view_model)
        self._setup_query_params_checkboxes(view_model)
        self._setup_header_checkboxes(view_model)
        self._setup_body_params_checkboxes(view_model)

    """ Private """

    def _reset_layout(self):
        self.box_layout.removeWidget(self.info_label)
        self.box_layout.removeWidget(self.path_param_values_label)
        self.box_layout.removeWidget(self.form_widget)
        self.info_label = QWidget()
        self.info_layout = QVBoxLayout()
        self.info_label.setLayout(self.info_layout)
        self.setLayout(self.box_layout)

    def _reset_input_form(self):
        self.form_widget = QWidget()
        self.form_layout = QFormLayout()
        self.form_layout.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.form_widget.setMinimumWidth(300)
        self.form_widget.setLayout(self.form_layout)
        self.box_layout.addWidget(self.path_param_values_label)
        self.box_layout.addWidget(self.form_widget)
        self.box_layout.addWidget(self.info_label)

    def _setup_path_params_checkboxes(self, view_model):
        if view_model.request_content.path_params:
            for path_param in view_model.request_content.path_params:
                is_checked = view_model.dynamic_values[ParameterType.PATH_PARAM]
                self._add_check_box(ParameterType.PATH_PARAM, path_param, is_checked)

    def _setup_query_params_checkboxes(self, view_model):
        if view_model.request_content.query_params:
            for query_param in view_model.request_content.query_params:
                is_checked = (
                    query_param in view_model.dynamic_values[ParameterType.QUERY_PARAM]
                )
                self._add_check_box(ParameterType.QUERY_PARAM, query_param, is_checked)

    def _setup_header_checkboxes(self, view_model):
        for header in view_model.request_content.headers:
            is_checked = header in view_model.dynamic_values[ParameterType.HEADER]
            self._add_check_box(ParameterType.HEADER, header, is_checked)

    def _setup_path_params_input_view(self, view_model):
        if view_model.request_content.path_params:
            self.path_param_values_label.setVisible(True)
            for path_param in view_model.request_content.path_params:
                self._add_path_param_row(path_param)
        else:
            self.path_param_values_label.setVisible(False)

    def _setup_body_params_checkboxes(self, view_model):
        if view_model.request_content.body_param_rows:
            for param_name in view_model.request_content.param_names:
                is_checked = (
                    param_name[0] in view_model.dynamic_values[ParameterType.BODY_PARAM]
                )
                self._add_check_box(ParameterType.BODY_PARAM, param_name[0], is_checked)

    def _add_check_box(self, param_type, title, is_checked):
        check_box = QCheckBox(param_type.value + " - " + title)
        if is_checked:
            check_box.setChecked(True)
        self._check_boxes.append(check_box)
        check_box.stateChanged.connect(self._on_dynamic_parameter_selection_change)
        self.info_layout.addWidget(check_box)

    def _add_path_param_row(self, param_name):
        path_param_line_edit = QLineEdit()
        self._path_param_lines.append(path_param_line_edit)
        self.form_layout.addRow(param_name + " = ", path_param_line_edit)
        if param_name in self.presenter.path_parameters_dictionary:
            text = self.presenter.path_parameters_dictionary[param_name]
            path_param_line_edit.setText(text)
        path_param_line_edit.textChanged.connect(self._on_path_param_line_edit_change)

    def _on_path_param_line_edit_change(self):
        params = {}
        for index, line in enumerate(self._path_param_lines):
            param_name = (
                self.form_layout.itemAt(index, 0).widget().text().replace(" = ", "")
            )
            param_value = line.text()
            params[param_name] = param_value
        self.presenter.on_path_param_line_edit_change(params)

    def _on_dynamic_parameter_selection_change(self):
        selected = set()
        for box in self._check_boxes:
            if box.isChecked():
                selected.add(box.text())
        self.presenter.on_dynamic_parameter_selection_change(selected)
