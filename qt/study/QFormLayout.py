import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


def window():
    app = QApplication(sys.argv)
    win = QWidget()

    # 创建姓名标签和输入框
    l1 = QLabel("Name")
    nm = QLineEdit()

    # 创建地址标签和两个地址输入框
    l2 = QLabel("Address")
    add1 = QLineEdit()
    add2 = QLineEdit()

    # 创建表单布局
    fbox = QFormLayout()
    fbox.addRow(l1, nm)

    # 创建垂直布局用于地址输入框
    vbox = QVBoxLayout()
    vbox.addWidget(add1)
    vbox.addWidget(add2)
    fbox.addRow(l2, vbox)

    # 创建水平布局用于性别单选按钮
    hbox = QHBoxLayout()
    r1 = QRadioButton("Male")
    r2 = QRadioButton("Female")
    hbox.addWidget(r1)
    hbox.addWidget(r2)
    hbox.addStretch()
    fbox.addRow(QLabel("Sex"), hbox)

    # 提交按钮
    submit_button = QPushButton("Submit")
    submit_button.clicked.connect(
        lambda: submit({
            "name": nm.text(),
            "add1": add1.text(),
            "add2": add2.text(),
            "sex": "Male" if r1.isChecked() else "Female" if r2.isChecked() else "",
        })
    )

    # 取消按钮
    cancel_button = QPushButton("Cancel")
    cancel_button.clicked.connect(lambda: cancel(nm, add1, add2, r1, r2))

    fbox.addRow(submit_button, cancel_button)

    win.setLayout(fbox)
    win.setWindowTitle("PyQt")
    win.show()
    sys.exit(app.exec_())


def submit(form: dict):
    print("Form submitted:", form)


def cancel(name_input, address1, address2, male_button, female_button):
    name_input.clear()
    address1.clear()
    address2.clear()
    male_button.setChecked(False)
    female_button.setChecked(False)
    print("Form cleared")


if __name__ == '__main__':
    window()
