from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
import os
import sys

homepage = QUrl("https://google.com")


class BrowserWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__()

        # set geometry and initial title
        self.setWindowTitle("Oof Browser")

        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)

        self.browser.setUrl(homepage)
        self.browser.urlChanged.connect(self.update_url_bar)
        self.browser.loadFinished.connect(self.update_title_bar)
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.navbar = QToolBar("Navigation")
        self.addToolBar(self.navbar)

        self.back = QAction("Back")
        self.back.triggered.connect(self.browser.back)
        self.back.setStatusTip("Go back to previous page")
        self.forward = QAction("Forward")
        self.forward.triggered.connect(self.browser.forward)
        self.forward.setStatusTip("Go forward to next page")
        self.refresh = QAction("Refresh")
        self.refresh.triggered.connect(self.browser.reload)
        self.home = QAction("Home")
        self.home.triggered.connect(self.navigate_home)
        self.home.setStatusTip("Go to homepage")

        self.url_bar = QLineEdit(self)
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        self.stop = QAction("Stop")
        self.stop.triggered.connect(self.browser.stop)
        self.stop.setStatusTip("Stop loading")

        for _ in [self.back, self.forward, self.refresh, self.home]:
            self.navbar.addAction(_)
        self.navbar.addWidget(self.url_bar)
        self.navbar.addAction(self.stop)

    def navigate_home(self):
        self.browser.setUrl(homepage)

    def navigate_to_url(self):
        target_url = QUrl(self.url_bar.text())

        if target_url.scheme() == "":
            target_url.setScheme("https")

        self.browser.setUrl(target_url)

    # happens if the page redirects, and url changes without input
    def update_url_bar(self, q):
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)

    def update_title_bar(self):
        self.setWindowTitle(f'{self.browser.page().title()} - Oof Browser')


if __name__ == '__main__':
    root_app = QApplication(sys.argv)
    browser_window = BrowserWindow()
    browser_window.show()
    root_app.exec_()
