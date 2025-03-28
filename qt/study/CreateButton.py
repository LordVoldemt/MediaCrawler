from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys

W_WIDTH = 400
W_HEIGHT = 400
W_X = 725
W_Y = 350


class CreateButton:
    def __init__(self, window, text, width, height, x, y):
        self.button = QPushButton(window)
        self.button.setText(text)
        self.button.resize(width, height)
        self.button.move(x, y)

    def get_instance(self):
        return self.button


class MyWin(QMainWindow):
    def __init__(self):
        super(MyWin, self).__init__()
        self.init()
        self.show()

    def writetextbox(self):
        self.textbox.setPlainText("test")

    def textboxcreate(self):
        self.textbox = QPlainTextEdit(self)
        self.textbox.move(150, 25)
        self.textbox.resize(75, 25)

    def init(self):
        self.resize(W_WIDTH, W_HEIGHT)
        self.move(W_X, W_Y)
        self.setWindowTitle('QlistWidget Example')

        self.mylist = QListWidget(self)
        self.mylist.setGeometry(5, 5, 135, 250)

        self.textbox = QPlainTextEdit(self)
        self.textbox.move(145, 5)
        self.textbox.resize(125, 25)

        self.button_add_item = CreateButton(self, "Add Item", 120, 25, 275, 5).get_instance()
        self.button_add_item.clicked.connect(self.additem)

        self.button_remove_item = CreateButton(self, "Remove Item", 250, 25, 145, 35).get_instance()
        self.button_remove_item.clicked.connect(self.delitem)

        self.mylist.itemDoubleClicked.connect(self.DoubleClicked_to_edit)

    def additem(self):
        if self.textbox.toPlainText() == "" or self.textbox.toPlainText() is None:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setText("Item cannot be empty")
            msgbox.setWindowTitle("Error")
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.exec()
        else:
            self.mylist.addItem(QListWidgetItem(self.textbox.toPlainText()))
            self.textbox.setPlainText(None)

    def delitem(self):
        selected_row = self.mylist.currentRow()
        item = self.mylist.takeItem(selected_row)
        del item

    def DoubleClicked_to_edit(self, item):
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        if not item.isSelected():
            item.setSelected(True)


app = QApplication(sys.argv)
win = MyWin()
sys.exit(app.exec_())

