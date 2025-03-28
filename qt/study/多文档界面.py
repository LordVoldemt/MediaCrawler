import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):
    count = 0  # 子窗口计数器，用于生成唯一子窗口标题

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)  # 调用父类构造函数
        self.mdi = QMdiArea()  # 创建MDI区域(多文档界面容器)
        self.setCentralWidget(self.mdi)  # 将MDI区域设置为主窗口中心部件
        bar = self.menuBar()  # 获取主窗口菜单栏

        # 创建File菜单并添加动作项
        file = bar.addMenu("File")
        file.addAction("New")  # 添加新建子窗口动作
        file.addAction("cascade")  # 添加层叠排列动作
        file.addAction("Tiled")  # 添加平铺排列动作
        # 连接菜单项触发信号到处理函数
        file.triggered[QAction].connect(self.windowaction)
        self.setWindowTitle("MDI demo")  # 设置主窗口标题

    def windowaction(self, q):
        print("triggered")  # 调试输出，显示菜单项被触发

        if q.text() == "New":
            # 新建子窗口逻辑
            MainWindow.count = MainWindow.count + 1  # 递增计数器
            sub = QMdiSubWindow()  # 创建子窗口
            sub.setWidget(QTextEdit())  # 在子窗口中添加文本编辑器部件
            sub.setWindowTitle("subwindow" + str(MainWindow.count))  # 设置子窗口标题
            self.mdi.addSubWindow(sub)  # 将子窗口添加到MDI区域
            sub.show()  # 显示子窗口

        if q.text() == "cascade":
            self.mdi.cascadeSubWindows()  # 层叠排列所有子窗口

        if q.text() == "Tiled":
            self.mdi.tileSubWindows()  # 平铺排列所有子窗口


def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
