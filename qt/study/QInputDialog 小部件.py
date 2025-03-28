import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class inputdialogdemo(QWidget):
    def __init__(self, parent=None):
        super(inputdialogdemo, self).__init__(parent)  # 调用父类QWidget的构造函数

        layout = QFormLayout()  # 创建一个表单布局
        self.btn = QPushButton("Choose from list")  # 创建选择列表按钮
        self.btn.clicked.connect(self.getItem)  # 连接按钮点击信号到getItem方法

        self.le = QLineEdit()  # 创建用于显示选择结果的文本框
        layout.addRow(self.btn, self.le)  # 将按钮和文本框添加到布局中

        self.btn1 = QPushButton("get name")  # 创建获取姓名按钮
        self.btn1.clicked.connect(self.gettext)  # 连接按钮点击信号到gettext方法

        self.le1 = QLineEdit()  # 创建用于显示姓名输入结果的文本框
        layout.addRow(self.btn1, self.le1)  # 将按钮和文本框添加到布局中

        self.btn2 = QPushButton("Enter an integer")  # 创建输入整数按钮
        self.btn2.clicked.connect(self.getint)  # 连接按钮点击信号到getint方法

        self.le2 = QLineEdit()  # 创建用于显示整数输入结果的文本框
        layout.addRow(self.btn2, self.le2)  # 将按钮和文本框添加到布局中

        self.setLayout(layout)  # 设置窗口的主布局
        self.setWindowTitle("Input Dialog demo")  # 设置窗口标题

    def getItem(self):
        items = ("C", "C++", "Java", "Python")  # 定义可选语言列表

        # 弹出列表选择对话框
        item, ok = QInputDialog.getItem(
            self, "select input dialog", "list of languages", items, 0, False
        )

        if ok and item:  # 如果用户选择了有效项
            self.le.setText(item)  # 在文本框中显示选择结果

    def gettext(self):
        # 弹出文本输入对话框
        text, ok = QInputDialog.getText(self, 'Text Input Dialog', 'Enter your name:')

        if ok:  # 如果用户确认输入
            self.le1.setText(str(text))  # 在文本框中显示输入的姓名

    def getint(self):
        # 弹出整数输入对话框
        num, ok = QInputDialog.getInt(self, "integer input dualog", "enter a number")

        if ok:  # 如果用户确认输入
            self.le2.setText(str(num))  # 在文本框中显示输入的整数


def main():
    app = QApplication(sys.argv)
    ex = inputdialogdemo()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
