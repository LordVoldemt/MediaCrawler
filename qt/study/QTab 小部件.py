import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class tabdemo(QTabWidget):
    """自定义标签页控件，继承自QTabWidget"""

    def __init__(self, parent=None):
        """初始化标签页控件"""
        super(tabdemo, self).__init__(parent)  # 调用父类构造函数
        # 创建三个标签页
        self.tab1 = QWidget()  # 第一个标签页
        self.tab2 = QWidget()  # 第二个标签页
        self.tab3 = QWidget()  # 第三个标签页

        # 添加标签页到控件
        self.addTab(self.tab1, "Tab 1")  # 添加标签1
        self.addTab(self.tab2, "Tab 2")  # 添加标签2
        self.addTab(self.tab3, "Tab 3")  # 添加标签3

        # 初始化各标签页UI
        self.tab1UI()  # 初始化第一个标签页UI
        self.tab2UI()  # 初始化第二个标签页UI
        self.tab3UI()  # 初始化第三个标签页UI

        self.setWindowTitle("tab demo")  # 设置窗口标题

    def tab1UI(self):
        """设置第一个标签页的UI布局"""
        layout = QFormLayout()  # 创建表单布局
        layout.addRow("Name", QLineEdit())  # 添加姓名输入行
        layout.addRow("Address", QLineEdit())  # 添加地址输入行
        self.setTabText(0, "Contact Details")  # 设置标签页标题
        self.tab1.setLayout(layout)  # 应用布局到标签页

    def tab2UI(self):
        """设置第二个标签页的UI布局"""
        layout = QFormLayout()  # 创建表单布局
        sex = QHBoxLayout()  # 创建水平布局用于性别选择
        sex.addWidget(QRadioButton("Male"))  # 添加男性单选按钮
        sex.addWidget(QRadioButton("Female"))  # 添加女性单选按钮
        layout.addRow(QLabel("Sex"), sex)  # 添加性别选择行
        layout.addRow("Date of Birth", QLineEdit())  # 添加出生日期输入行
        self.setTabText(1, "Personal Details")  # 设置标签页标题
        self.tab2.setLayout(layout)  # 应用布局到标签页

    def tab3UI(self):
        """设置第三个标签页的UI布局"""
        layout = QHBoxLayout()  # 创建水平布局
        layout.addWidget(QLabel("subjects"))  # 添加科目标签
        layout.addWidget(QCheckBox("Physics"))  # 添加物理复选框
        layout.addWidget(QCheckBox("Maths"))  # 添加数学复选框
        self.setTabText(2, "Education Details")  # 设置标签页标题
        self.tab3.setLayout(layout)  # 应用布局到标签页


def main():
    # 创建Qt应用程序对象，sys.argv用于接收命令行参数
    app = QApplication(sys.argv)

    # 创建标签页窗口实例
    ex = tabdemo()

    # 显示主窗口
    ex.show()

    # 进入Qt主事件循环，exec_()会阻塞直到应用退出
    # sys.exit()确保应用退出时返回正确状态码
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
