import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


def window():
    # 创建QApplication实例，管理应用程序的主控制流
    app = QApplication(sys.argv)
    # 创建主窗口部件
    win = QWidget()
    # 创建网格布局管理器
    grid = QGridLayout()

    # 使用双重循环创建4x4的按钮网格
    for i in range(1, 5):  # 行循环(1-4)
        for j in range(1, 5):  # 列循环(1-4)
            # 创建按钮并添加到网格布局，按钮文本为"B"+行号+列号
            grid.addWidget(QPushButton("B" + str(i) + str(j)), i, j)

    # 将网格布局设置到主窗口
    win.setLayout(grid)
    # 设置窗口位置和大小(x, y, width, height)
    win.setGeometry(100, 100, 200, 100)
    # 设置窗口标题
    win.setWindowTitle("PyQt")
    # 显示窗口
    win.show()
    # 进入应用程序主事件循环
    sys.exit(app.exec_())


if __name__ == '__main__':
    window()
