import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class stackedExample(QWidget):
    def __init__(self):
        super(stackedExample, self).__init__()
        # 左侧列表控件，用于切换不同页面
        self.leftlist = QListWidget()
        self.leftlist.insertItem(0, 'Contact')  # 添加第一个列表项
        self.leftlist.insertItem(1, 'Personal')  # 添加第二个列表项
        self.leftlist.insertItem(2, 'Educational')  # 添加第三个列表项

        # 创建三个堆叠页面
        self.stack1 = QWidget()  # 联系人信息页面
        self.stack2 = QWidget()  # 个人信息页面
        self.stack3 = QWidget()  # 教育信息页面

        # 初始化各个页面的UI
        self.stack1UI()
        self.stack2UI()
        self.stack3UI()

        # 创建堆叠窗口部件并添加三个页面
        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack2)
        self.Stack.addWidget(self.stack3)

        # 创建水平布局，左侧是列表，右侧是堆叠页面
        hbox = QHBoxLayout(self)
        hbox.addWidget(self.leftlist)
        hbox.addWidget(self.Stack)

        self.setLayout(hbox)  # 设置主窗口布局
        # 连接列表项切换信号到显示函数
        self.leftlist.currentRowChanged.connect(self.display)
        self.setGeometry(300, 50, 10, 10)  # 设置窗口位置和大小
        self.setWindowTitle('StackedWidget demo')  # 设置窗口标题
        self.show()  # 显示窗口

    def stack1UI(self):
        """初始化联系人信息页面的UI"""
        layout = QFormLayout()  # 表单布局
        layout.addRow("Name", QLineEdit())  # 姓名输入框
        layout.addRow("Address", QLineEdit())  # 地址输入框
        self.stack1.setLayout(layout)  # 设置页面布局

    def stack2UI(self):
        """初始化个人信息页面的UI"""
        layout = QFormLayout()
        sex = QHBoxLayout()  # 水平布局用于单选按钮
        sex.addWidget(QRadioButton("Male"))  # 男性单选按钮
        sex.addWidget(QRadioButton("Female"))  # 女性单选按钮
        layout.addRow(QLabel("Sex"), sex)  # 添加性别选择行
        layout.addRow("Date of Birth", QLineEdit())  # 生日输入框
        self.stack2.setLayout(layout)

    def stack3UI(self):
        """初始化教育信息页面的UI"""
        layout = QHBoxLayout()  # 水平布局
        layout.addWidget(QLabel("subjects"))  # 科目标签
        layout.addWidget(QCheckBox("Physics"))  # 物理复选框
        layout.addWidget(QCheckBox("Maths"))  # 数学复选框
        self.stack3.setLayout(layout)

    def display(self, i):
        """根据列表选择切换显示对应的页面"""
        self.Stack.setCurrentIndex(i)  # 设置当前显示的页面索引


def main():
    app = QApplication(sys.argv)
    ex = stackedExample()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
