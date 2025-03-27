
import sys

from PyQt5.QtCore import *

from PyQt5.QtGui import *

from PyQt5.QtWidgets import *



class Form(QDialog):
    """
    这是类的构造函数，在创建类实例时自动调用
    self 参数代表类的实例本身
    parent=None 表示这个参数是可选的，默认值为 None
    """
    def __init__(self, parent=None):
        """
        这行代码的作用是：
        调用父类(QDialog)的构造函数
        确保 Qt 的父子关系系统正常工作
        当父窗口被销毁时，子窗口也会自动销毁
        如果 parent 为 None，表示这是一个顶级窗口，没有父窗口
        """
        super(Form, self).__init__(parent)

        # 创建垂直布局
        layout = QVBoxLayout()

        # 创建可切换状态的按钮1
        self.b1 = QPushButton("Button1")
        self.b1.setCheckable(True)  # 设置为可选中状态
        self.b1.toggle()  # 切换按钮状态
        self.b1.clicked.connect(lambda: self.whichbtn(self.b1))  # 绑定点击事件
        self.b1.clicked.connect(self.btnstate)  # 绑定状态变化事件
        layout.addWidget(self.b1)

        # 创建带图标的按钮2
        self.b2 = QPushButton()
        self.b2.setIcon(QIcon(QPixmap("python.jpg")))  # 设置按钮图标
        self.b2.clicked.connect(lambda: self.whichbtn(self.b2))
        layout.addWidget(self.b2)

        self.setLayout(layout)  # 设置主布局

        # 创建禁用按钮3
        self.b3 = QPushButton("Disabled")
        self.b3.setEnabled(False)  # 禁用按钮
        layout.addWidget(self.b3)

        # 创建默认按钮4
        self.b4 = QPushButton("&Default")
        self.b4.setDefault(True)  # 设置为默认按钮(可通过Enter键触发)
        self.b4.clicked.connect(lambda: self.whichbtn(self.b4))
        layout.addWidget(self.b4)

        self.setWindowTitle("Button demo")  # 设置窗口标题

    def btnstate(self):
        # 按钮状态变化处理函数
        if self.b1.isChecked():
            print("button pressed")  # 按钮被按下
        else:
            print("button released")  # 按钮被释放

    def whichbtn(self, b):
        # 按钮点击处理函数
        print("clicked button is " + b.text())  # 输出被点击按钮的文本



def main():
    # 创建Qt应用程序对象，sys.argv用于接收命令行参数
    app = QApplication(sys.argv)

    # 创建Form对话框实例
    ex = Form()

    # 显示对话框窗口
    ex.show()

    # 进入Qt应用程序主循环，exec_()方法会阻塞直到应用程序退出
    # sys.exit()确保应用程序退出时返回正确的状态码
    sys.exit(app.exec_())




if __name__ == '__main__':

    main()

