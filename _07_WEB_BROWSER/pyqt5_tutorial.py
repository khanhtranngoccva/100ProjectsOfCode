import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class TextPromptWindow(QWidget):
    def __init__(self, window_name="PyQt5 Window", text_prompt="", position=(100, 100), size=(640, 480)):
        super().__init__()
        self.setWindowTitle(window_name)
        self.setGeometry(*position, *size)
        label1 = QLabel(self)
        label1.setText(text_prompt)


def main():
    root = QApplication([])
    window1 = TextPromptWindow("First test", "Hello World!", (200, 200), (400, 200))
    window1.show()
    root.exec()

if __name__ == '__main__':
    main()