from curl2swift.layers.presentation.main_window import MainWindow
import sys

from PyQt5.QtWidgets import QApplication, QDesktopWidget

from curl2swift.layers.presentation.content_view import ContentView


class Application:
    @classmethod
    def run(cls):
        app = QApplication(sys.argv)
        screen = app.primaryScreen()
        size = screen.size()
        screen_width = size.width()
        content = ContentView(screen_width)
        cls.window = content

        main_window = MainWindow()
        main_window.setup(lambda label: cls.handle_menu_button_tap(cls, label))
        main_window.setCentralWidget(cls.window)
        main_window.show()
        main_window.resize(screen.size())

        frame_geometry = main_window.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center)
        main_window.move(frame_geometry.topLeft())
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
