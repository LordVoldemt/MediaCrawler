import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
# QBoxLayout 类垂直或水平排列小部件。它的派生类是 QVBoxLayout（用于垂直排列小部件）和 QHBoxLayout（用于水平排列小部件）

def window():
    # 创建QApplication实例，管理应用程序的控制流和主要设置
    app = QApplication(sys.argv)
    # 创建一个QWidget窗口实例
    win = QWidget()
    # 创建两个按钮控件
    b1 = QPushButton("Button1")
    b2 = QPushButton("Button2")
    b2.clicked.connect(b2_clicked)
    # 创建垂直布局管理器
    vbox = QVBoxLayout()
    # 将第一个按钮添加到布局中
    vbox.addWidget(b1)
    # 添加可伸缩空间
    vbox.addStretch()
    # 将第二个按钮添加到布局中
    vbox.addWidget(b2)
    # 将布局设置到窗口上
    win.setLayout(vbox)
    # 设置窗口标题
    win.setWindowTitle("PyQt")
    # 显示窗口
    win.show()
    # 进入应用程序主循环
    sys.exit(app.exec_())

def b1_clicked():
    print("Button 1 clicked")


def b2_clicked():
    print("Button 2 clicked")


if __name__ == '__main__':
    window()
