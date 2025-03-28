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
from QTableWidget import *

def window():
    app = QApplication(sys.argv)  # 创建应用程序对象
    win = QWidget()  # 创建主窗口部件
    # 设置窗口win的几何位置和大小，起始坐标为(100, 100)，宽度为200，高度为100
    win.setGeometry(800, 400, 1024, 768)
    # 创建姓名标签和输入框
    l1 = QLabel("激活码")  # 激活码标签
    activation_code = QLineEdit()  # 激活码输入框

    # 创建表单布局
    fbox = QFormLayout()  # 创建表单布局管理器
    fbox.addRow(l1, activation_code)  # 添加姓名输入框到表单

    # 提交按钮
    submit_button = QPushButton("登录")  # 创建提交按钮
    submit_button.clicked.connect(
        lambda: submit({  # 绑定提交事件，点击时调用 submit 方法
            "activation_code": activation_code.text(),  # 获取姓名输入框的值
        },win)
    )

    # 取消按钮
    cancel_button = QPushButton("取消")  # 创建取消按钮
    cancel_button.clicked.connect(lambda: cancel(activation_code))  # 绑定取消事件，点击时清空表单

    fbox.addRow(submit_button, cancel_button)  # 添加提交和取消按钮到表单

    win.setLayout(fbox)  # 将表单布局设置到窗口
    win.setWindowTitle("小红书获客系统v1.00")  # 设置窗口标题
    win.show()  # 显示窗口
    sys.exit(app.exec_())  # 进入应用程序主循环


def submit(form: dict,win):
    """提交表单时调用，打印表单内容"""
    print("Form submitted:", form)
    # 登录之后，校驗激活码是否正确，正确则跳转到主页面，错误则弹出错误提示框
    if form["activation_code"] == "123456":
        print("激活码正确")
        # 在此处关闭win窗口
        win.close()
        # 跳转到主页面
        global ex  # 让 ex 成为全局变量，防止被垃圾回收
        # 创建标签页窗口实例
        ex = tab_demo()
        # 显示主窗口
        ex.show()



def cancel(name_input):
    """取消按钮点击时调用，清空所有输入框和单选按钮"""
    name_input.clear()  # 清空姓名输入框
    print("Form cleared")  # 输出清空提示


if __name__ == '__main__':
    window()  # 运行窗口
