import sys

from PyQt5.QtWidgets import *


# 主要优化点：
# 性别单选按钮的值：
#
# submit() 方法获取 r1.isChecked() 或 r2.isChecked()，确定选中的性别。
#
# 如果没有选中任何按钮，则性别为空字符串 ""。
#
# 清空表单值：
#
# cancel() 方法被 cancel_button 触发，清空所有输入框 clear()。
#
# 取消选中单选按钮 setChecked(False)。
#
# 这样，点击 Submit 按钮时，会提交所有字段，包括性别；点击 Cancel 按钮时，会清空表单。

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


def window():
    app = QApplication(sys.argv)  # 创建应用程序对象
    win = QWidget()  # 创建主窗口部件

    # 创建姓名标签和输入框
    l1 = QLabel("Name")  # 姓名标签
    nm = QLineEdit()  # 姓名输入框

    # 创建地址标签和两个地址输入框
    l2 = QLabel("Address")  # 地址标签
    add1 = QLineEdit()  # 地址输入框1
    add2 = QLineEdit()  # 地址输入框2

    # 创建表单布局
    fbox = QFormLayout()  # 创建表单布局管理器
    fbox.addRow(l1, nm)  # 添加姓名输入框到表单

    # 创建垂直布局用于存放多个地址输入框
    vbox = QVBoxLayout()
    vbox.addWidget(add1)  # 添加第一个地址输入框
    vbox.addWidget(add2)  # 添加第二个地址输入框
    fbox.addRow(l2, vbox)  # 将地址行(标签 + 垂直布局)添加到表单

    # 创建水平布局用于性别单选按钮
    hbox = QHBoxLayout()
    r1 = QRadioButton("Male")  # 男性单选按钮
    r2 = QRadioButton("Female")  # 女性单选按钮
    hbox.addWidget(r1)  # 添加男性单选按钮
    hbox.addWidget(r2)  # 添加女性单选按钮
    hbox.addStretch()  # 添加伸缩空间，让单选按钮靠左
    fbox.addRow(QLabel("Sex"), hbox)  # 将性别行(标签 + 水平布局)添加到表单

    # 提交按钮
    submit_button = QPushButton("Submit")  # 创建提交按钮
    submit_button.clicked.connect(
        lambda: submit({  # 绑定提交事件，点击时调用 submit 方法
            "name": nm.text(),  # 获取姓名输入框的值
            "add1": add1.text(),  # 获取地址1输入框的值
            "add2": add2.text(),  # 获取地址2输入框的值
            "sex": "Male" if r1.isChecked() else "Female" if r2.isChecked() else "",  # 获取选中的性别
        })
    )

    # 取消按钮
    cancel_button = QPushButton("Cancel")  # 创建取消按钮
    cancel_button.clicked.connect(lambda: cancel(nm, add1, add2, r1, r2))  # 绑定取消事件，点击时清空表单

    fbox.addRow(submit_button, cancel_button)  # 添加提交和取消按钮到表单

    win.setLayout(fbox)  # 将表单布局设置到窗口
    win.setWindowTitle("PyQt")  # 设置窗口标题
    win.show()  # 显示窗口
    sys.exit(app.exec_())  # 进入应用程序主循环


def submit(form: dict):
    """提交表单时调用，打印表单内容"""
    print("Form submitted:", form)


def cancel(name_input, address1, address2, male_button, female_button):
    """取消按钮点击时调用，清空所有输入框和单选按钮"""
    name_input.clear()  # 清空姓名输入框
    address1.clear()  # 清空地址1输入框
    address2.clear()  # 清空地址2输入框
    male_button.setChecked(False)  # 取消选中男性单选按钮
    female_button.setChecked(False)  # 取消选中女性单选按钮
    print("Form cleared")  # 输出清空提示


if __name__ == '__main__':
    window()  # 运行窗口

