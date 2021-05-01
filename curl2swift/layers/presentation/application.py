from curl2swift.layers.presentation.main_window import MainWindow
import sys

from PyQt5.QtWidgets import QApplication

from curl2swift.layers.presentation.content_view import ContentView


class Application:
    @classmethod
    def run(cls):
        app = QApplication(sys.argv)
        screen = app.primaryScreen()
        size = screen.size()
        screen_width = size.width()
        cls.window = ContentView(screen_width)
        cls.window.setMaximumWidth(size.width())

        main_window = MainWindow()
        main_window.setup(lambda label: cls.handle_menu_button_tap(cls, label))
        main_window.setCentralWidget(cls.window)
        main_window.show()
        sys.exit(app.exec_())

    def handle_menu_button_tap(self, label):
        if label == "request_view":
            self.window.left_half_frame.show()
            self.window.templates_view.hide()
        elif label == "templates_view":
            self.window.left_half_frame.hide()
            self.window.templates_view.show()
            self.window.templates_view.setFocus()
