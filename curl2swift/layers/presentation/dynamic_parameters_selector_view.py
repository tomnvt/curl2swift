
from curl2swift.layers.presentation.content_presenter import WindowViewModel
from PyQt5.QtWidgets import (
    QCheckBox,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class DynamicParamsSelectorView(QWidget):

    _selected = set()

    def __init__(self, presenter):
        super().__init__()
        self.presenter = presenter
        self.box_layout = QVBoxLayout()
        self.info_label = QWidget()
        self.info_layout = QVBoxLayout()
        self.setLayout(self.box_layout)
     
    _dheck_boxes = []

    def update(self, view_model: WindowViewModel):
        self._dheck_boxes = []
        self.box_layout.removeWidget(self.info_label)
        self.info_label = QWidget()
        self.info_layout = QVBoxLayout()
        self.info_label.setLayout(self.info_layout)
        self.box_layout.addWidget(self.info_label)
        for value_type in view_model.dynamic_values:
            for value in view_model.dynamic_values[value_type]:
                print("value_type + ' - ' + value")
                print(value_type + ' - ' + value)
                self._selected.add(value_type + ' - ' + value)

        self.info_layout.addWidget(QLabel("Which values are dynamic?"))

        for header in view_model.request_content.headers:
            self._add_check_box('HEADER', header)

        if view_model.request_content.query_params:
            for query_param in view_model.request_content.query_params:
                self._add_check_box('QUERY PARAM', query_param)

        if view_model.request_content.body_param_rows:
            for query_param in view_model.request_content.body_param_rows:
                self._add_check_box('BODY PARAM', query_param)


        self.setLayout(self.box_layout)

    def _add_check_box(self, param_type, title):
        check_box = QCheckBox(param_type + ' - ' + title)
        if param_type + ' - ' + title in self._selected:
            check_box.setChecked(True)
        self._dheck_boxes.append(check_box)
        check_box.stateChanged.connect(self._on_change)
        self.info_layout.addWidget(check_box)

    def _on_change(self):
        for box in self._dheck_boxes:
            if box.isChecked():
                self._selected.add(box.text())
            else:
                if box.text() in self._selected:
                    self._selected.remove(box.text())
        self.presenter.on_dynamic_parameter_selection_change(self._selected)
