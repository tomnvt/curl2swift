from PyQt5.QtWidgets import (
    QAction,
    QMainWindow,
)


class MainWindow(QMainWindow):
    def setup(self, on_menu_item_tap):
        menuBar = self.menuBar()

        editMenu = menuBar.addMenu("&View")

        self.request_view_action = QAction("Show request editor")
        self.request_view_action.triggered.connect(
            lambda: on_menu_item_tap("request_view")
        )
        editMenu.addAction(self.request_view_action)

        # TODO: Add Template editor
        self.templates_view_action = QAction("Show template editor")
        self.templates_view_action.triggered.connect(
            lambda: on_menu_item_tap("templates_view")
        )
        editMenu.addAction(self.templates_view_action)
