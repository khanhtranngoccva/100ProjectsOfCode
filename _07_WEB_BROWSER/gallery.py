# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gallery.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import os

from PyQt5 import QtCore, QtGui, QtWidgets


def get_photos():
    return [QtGui.QPixmap("gallery_photo/" + photo_name) for photo_name in os.listdir("gallery_photo")]


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 500, 801, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.back = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.back.setObjectName("back")
        self.horizontalLayout.addWidget(self.back)
        self.next = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.next.setObjectName("next")
        self.horizontalLayout.addWidget(self.next)
        self.photo_label = QtWidgets.QLabel(self.centralwidget)
        self.photo_label.setGeometry(QtCore.QRect(0, 0, 801, 481))
        self.photo_label.setObjectName("photo_label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.photos = get_photos()
        self.photo_count = len(self.photos)
        self.position = 0
        self.back.clicked.connect(lambda: self.update_photo(-1))
        self.next.clicked.connect(lambda: self.update_photo(1))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Image Gallery"))
        self.back.setText(_translate("MainWindow", "Back"))
        self.next.setText(_translate("MainWindow", "Next"))
        self.photo_label.setText(_translate("MainWindow", "TextLabel"))

    def update_photo(self, offset):
        self.show_popup(f'You moved {offset} images.')
        self.position += offset
        if self.position >= self.photo_count:
            self.position %= self.photo_count
        elif self.position < 0:
            self.position %= self.photo_count
        # print(self.position)
        self.photo_label.setPixmap(self.photos[self.position])

    def show_popup(self, text):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Tutorial on PyQt5")
        msg.setText(text)
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setStandardButtons(QtWidgets.QMessageBox.Close|QtWidgets.QMessageBox.Ignore)
        msg.setInformativeText("oof")
        msg.setDetailedText("ooooooffff")
        msg.buttonClicked.connect(self.popup_log)
        # msg.show()
        msg.exec_()

    def popup_log(self, i):
        print(i.text())

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
