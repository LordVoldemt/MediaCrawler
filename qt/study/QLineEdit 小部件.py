
import sys

from PyQt5.QtCore import *

from PyQt5.QtGui import *

from PyQt5.QtWidgets import *

def window():
    # 初始化Qt应用
    app = QApplication(sys.argv)
    # 创建主窗口
    win = QWidget()

    # 创建整数验证输入框
    e1 = QLineEdit()
    e1.setValidator(QIntValidator())  # 只允许输入整数
    e1.setMaxLength(4)  # 最大长度4个字符
    e1.setAlignment(Qt.AlignRight)  # 文本右对齐
    e1.setFont(QFont("Arial", 20))  # 设置字体和大小

    # 创建浮点数验证输入框
    e2 = QLineEdit()
    e2.setValidator(QDoubleValidator(0.99, 99.99, 2))  # 允许0.99-99.99范围的2位小数

    # 创建表单布局
    flo = QFormLayout()
    flo.addRow("integer validator", e1)  # 添加整数输入框
    flo.addRow("Double validator", e2)  # 添加浮点数输入框

    # 创建带输入掩码的电话号码输入框
    e3 = QLineEdit()
    e3.setInputMask('+99_9999_999999')  # 设置电话号码输入格式
    flo.addRow("Input Mask", e3)

    # 创建文本变化监听输入框
    e4 = QLineEdit()
    e4.textChanged.connect(textchanged)  # 绑定文本变化信号
    flo.addRow("Text changed", e4)

    # 创建密码输入框
    e5 = QLineEdit()
    e5.setEchoMode(QLineEdit.Password)  # 设置为密码模式
    flo.addRow("Password", e5)

    # 创建只读输入框
    e6 = QLineEdit("Hello Python")
    e6.setReadOnly(True)  # 设置为只读
    flo.addRow("Read Only", e6)

    # 绑定编辑完成信号
    e5.editingFinished.connect(enterPress)

    # 设置窗口布局并显示
    win.setLayout(flo)
    win.setWindowTitle("PyQt")
    win.show()

    # 启动应用事件循环
    sys.exit(app.exec_())



def textchanged(text):

    print (f"contents of text box: {text}")



def enterPress():

    print ("edited")



if __name__ == '__main__':

    window()

