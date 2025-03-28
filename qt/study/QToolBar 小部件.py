import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class tooldemo(QMainWindow):
    def __init__(self, parent=None):
        super(tooldemo, self).__init__(parent)  # 调用父类QMainWindow的构造函数
        layout = QVBoxLayout()  # 创建一个垂直布局管理器
        tb = self.addToolBar("File")  # 添加一个名为"File"的工具栏

        # 创建"新建"动作，设置图标和文本
        new = QAction(QIcon("new.bmp"), "new", self)
        tb.addAction(new)  # 将动作添加到工具栏

        # 创建"打开"动作，设置图标和文本
        open = QAction(QIcon("open.bmp"), "open", self)
        tb.addAction(open)  # 将动作添加到工具栏

        # 创建"保存"动作，设置图标和文本
        save = QAction(QIcon("save.bmp"), "save", self)
        tb.addAction(save)  # 将动作添加到工具栏

        # 连接工具栏动作触发信号到处理函数
        tb.actionTriggered[QAction].connect(self.toolbtnpressed)
        self.setLayout(layout)  # 设置主窗口的布局
        self.setWindowTitle("toolbar demo")  # 设置窗口标题

    def toolbtnpressed(self, a):
        # 工具栏按钮点击事件处理函数
        print("pressed tool button is", a.text())  # 打印被点击按钮的文本


def main():
    app = QApplication(sys.argv)

    ex = tooldemo()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
