import sys
from time import sleep

from PyQt5.QtCore import *

from PyQt5.QtGui import *

from PyQt5.QtWidgets import *

"""
是的，class checkdemo(QWidget) 表示一个继承关系。具体来说：
继承关系：
checkdemo 是子类
QWidget 是父类
使用 super(checkdemo, self).__init__(parent) 调用父类构造函数
继承带来的特性：
自动获得QWidget的所有功能（窗口显示、事件处理等）
可以重写父类方法（如本例没有重写）
可以添加新的属性和方法（如添加了btnstate方法）
"""
class checkdemo(QWidget):
    """演示QCheckBox使用的自定义窗口类"""
    def __init__(self, parent=None):
        """初始化复选框演示窗口"""
        super(checkdemo, self).__init__(parent)  # 调用父类构造函数

        # 创建水平布局
        layout = QHBoxLayout()

        # 创建第一个复选框
        self.b1 = QCheckBox("Button1")
        self.b1.setChecked(True)  # 默认选中状态
        # 连接状态变化信号到处理函数
        self.b1.stateChanged.connect(lambda: self.btnstate(self.b1))
        layout.addWidget(self.b1)  # 添加到布局

        # 创建第二个复选框
        self.b2 = QCheckBox("Button2")
        # 连接切换信号到处理函数
        self.b2.toggled.connect(lambda: self.btnstate(self.b2))
        layout.addWidget(self.b2)  # 添加到布局

        self.setLayout(layout)  # 设置窗口布局
        self.setWindowTitle("checkbox demo")  # 设置窗口标题

    def btnstate(self, b):
        """复选框状态变化处理函数"""
        if b.text() == "Button1":
            if b.isChecked():
                print(b.text() + " is selected")  # 按钮1被选中
            else:
                print(b.text() + " is deselected")  # 按钮1取消选中

        if b.text() == "Button2":
            if b.isChecked():
                print(b.text() + " is selected")  # 按钮2被选中
            else:
                print(b.text() + " is deselected")  # 按钮2取消选中


def main():
    # 创建QApplication实例，sys.argv用于接收命令行参数
    app = QApplication(sys.argv)

    # 创建checkdemo窗口实例
    ex = checkdemo()

    # 显示窗口
    ex.show()
    # 进入主事件循环，app.exec_()会阻塞直到应用退出
    # sys.exit()确保应用退出时返回正确的状态码
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
