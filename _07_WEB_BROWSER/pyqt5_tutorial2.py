from PyQt5.QtWidgets import *
import sys


class MyWindow(QWidget):
    def __init__(self, window_title="PyQt5 Window", geometry=(0, 0, 640, 480)):
        super().__init__()
        self.setWindowTitle(window_title)
        self.setGeometry(*geometry)
        self.init_ui()

    def init_ui(self):
        self.label = QLabel(self)
        self.label.setText("Hello I'm oof")
        self.label.move(50, 50)

        self.button = QPushButton(self)
        self.button.setText("Click me again!")
        self.button.clicked.connect(self.clicked)

    def clicked(self):
        self.label.setText("Hey you clicked the button!!!")
        self.label.adjustSize()


def onclick():
    print(1)


def window():
    app = QApplication(sys.argv)
    main_window = QWidget()
    main_window.setWindowTitle("OOF")
    main_window.setGeometry(0, 0, 640, 480)

    label1 = QLabel(main_window)
    label1.setText("oof")

    button1 = QPushButton(main_window)
    button1.setText("Press me!")
    button1.clicked.connect(onclick)

    main_window.show()

    # Pauses main thread and launches windows instead of exiting abruptly
    app.exec()


def main():
    root_app = QApplication(sys.argv)
    window_1 = MyWindow()
    window_1.show()
    root_app.exec()


if __name__ == '__main__':
    main()
