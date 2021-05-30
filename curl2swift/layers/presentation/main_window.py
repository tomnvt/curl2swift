from PyQt5.QtWidgets import (
    QAction,
    QMainWindow,
)


class MainWindow(QMainWindow):
    def setup(self, on_menu_item_tap):
        menuBar = self.menuBar()

        editMenu = menuBar.addMenu("&View")

        self.request_view_action = QAction("Toggle request editor visibility")
        self.request_view_action.triggered.connect(
            lambda: on_menu_item_tap("request_view")
        )
        editMenu.addAction(self.request_view_action)

        self.templates_view_action = QAction("Toggle output view visibility")
        self.templates_view_action.triggered.connect(
            lambda: on_menu_item_tap("output_view")
        )
        self.setWindowTitle("curl2swift")
        editMenu.addAction(self.templates_view_action)
