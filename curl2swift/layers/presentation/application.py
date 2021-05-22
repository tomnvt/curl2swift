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

        main_window = MainWindow()
        main_window.setup(lambda label: cls.handle_menu_button_tap(cls, label))
        main_window.setCentralWidget(cls.window)
        main_window.show()
        sys.exit(app.exec_())

    def handle_menu_button_tap(self, label):
        if label == "request_view":
            if self.window.left_half_frame.isVisible():
                self.window.left_half_frame.hide()
            else:
                self.window.left_half_frame.show()
        if label == "output_view":
            if self.window.tabs.isVisible():
                self.window.tabs.hide()
            else:
                self.window.tabs.show()
