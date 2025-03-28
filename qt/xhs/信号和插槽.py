import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


def window():
    # 创建一个QApplication实例，用于管理应用程序的控制流和主要设置
    app = QApplication(sys.argv)
    # 创建一个QDialog窗口实例，指定父窗口为None（这里需要传入parent参数，当前未传，后续可修改）
    win = QDialog()
    # 创建一个QPushButton实例，将其父窗口设置为win
    b1 = QPushButton(win)
    # 设置按钮b1的文本为"Button1"
    b1.setText("Button1")
    # 移动按钮b1到窗口内的指定位置 (50, 20)
    b1.move(50, 20)
    # 将按钮b1的clicked信号连接到b1_clicked函数，当按钮被点击时触发该函数
    b1.clicked.connect(b1_clicked)

    # 创建另一个QPushButton实例，将其父窗口设置为win
    b2 = QPushButton(win)
    # 设置按钮b2的文本为"Button2"
    b2.setText("Button2")
    # 移动按钮b2到窗口内的指定位置 (50, 50)
    b2.move(50, 50)
    # 将按钮b2的clicked信号连接到b2_clicked函数，当按钮被点击时触发该函数
    b2.clicked.connect(b2_clicked)

    # 新增关闭按钮
    close_btn = QPushButton(win)
    close_btn.setText("关闭窗口")
    close_btn.move(50, 80)
    close_btn.clicked.connect(win.close)  # 直接连接窗口的close方法

    # 设置窗口win的几何位置和大小，起始坐标为(100, 100)，宽度为200，高度为100
    win.setGeometry(800, 400, 1024, 768)

    # 设置窗口win的标题为"PyQt5"
    win.setWindowTitle("PyQt5")
    # 显示窗口win
    win.show()
    # 进入应用程序的主循环，并在窗口关闭时退出应用程序
    sys.exit(app.exec_())



def b1_clicked():
    print("Button 1 clicked")


def b2_clicked():
    print("Button 2 clicked")


if __name__ == '__main__':
    window()
