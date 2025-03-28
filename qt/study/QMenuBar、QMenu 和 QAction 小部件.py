import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


# 在PyQt5中，QMainWindow和QWidget都是用于创建GUI界面的基础类，但有以下关键区别：
# QWidget：
# 是所有用户界面对象的基类
# 轻量级窗口，适合简单对话框或自定义控件
# 需要手动添加布局和控件
# 没有预定义的菜单栏、状态栏等
# 示例用法：创建弹出窗口、工具窗口等
# QMainWindow：
# 是专为主窗口设计的高级类
# 继承自QWidget但增加了专门功能
# 预定义了：
# 菜单栏(menuBar)
# 工具栏(toolBar)
# 状态栏(statusBar)
# 中心部件(centralWidget)
# 停靠区域(dockWidgets)
# 适合应用程序的主窗口
# 示例用法：文本编辑器、IDE等复杂界面
# 选择建议：
# 简单界面 → 使用QWidget
# 需要菜单/工具栏的复杂主窗口 → 使用QMainWindow

class menudemo(QMainWindow):
    """演示菜单栏、菜单和动作的自定义主窗口类"""

    def __init__(self, parent=None):
        """初始化菜单演示窗口"""
        super(menudemo, self).__init__(parent)  # 调用父类构造函数

        # 创建水平布局(实际未使用，QMainWindow有默认布局)
        layout = QHBoxLayout()

        # 获取主窗口的菜单栏
        bar = self.menuBar()
        # 添加"File"主菜单
        file = bar.addMenu("File")
        file.addAction("New")  # 添加"New"动作
        # 创建带快捷键的"Save"动作
        save = QAction("Save", self)
        save.setShortcut("Ctrl+S")  # 设置快捷键
        file.addAction(save)

        # 在File菜单下添加Edit子菜单
        edit = file.addMenu("Edit")
        edit.addAction("copy")  # 添加"copy"动作
        edit.addAction("paste")  # 添加"paste"动作

        # 创建"Quit"动作
        quit = QAction("Quit", self)
        file.addAction(quit)

        # 连接菜单触发信号到处理函数
        file.triggered[QAction].connect(self.processtrigger)

        view = bar.addMenu("视图")
        tool_window = view.addAction("工具窗口")
        appearance = view.addAction("外观")
        view.triggered[QAction].connect(self.process_view)
        # 设置布局和窗口标题
        self.setLayout(layout)  # 实际QMainWindow不需要手动设置布局
        self.setWindowTitle("menu demo")

    """
    具体解释：
    q 是自动传入的 QAction 对象
    当用户点击菜单项时，Qt会自动将对应的QAction对象作为参数传入
    参数名q是自定义的(可以是任何合法变量名)，但通常建议使用更有意义的名称如action
    通过q可以：
    获取动作文本：q.text()
    检查是否可选中：q.isCheckable()
    获取图标：q.icon()
    获取快捷键：q.shortcut()
    信号连接方式决定了参数类型：
    """

    def processtrigger(self, q):
        """菜单动作触发处理函数"""
        print(q.text() + " is triggered")  # 打印被触发的动作文本

    def process_view(self, q):
        print(q.text() + " is process_view")


def main():
    app = QApplication(sys.argv)
    ex = menudemo()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
