import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
# QLabel对象充当占位符以显示不可编辑的文本或图像，或动画 GIF 电影。它也可以用作其他小部件的助记键。标签上可以显示纯文本、超链接或富文本。
# 下表列出了 QLabel 类中定义的重要方法 -
# 下面给出了 QLabel 最常用的方法。
def window():
    # 初始化Qt应用
    app = QApplication(sys.argv)
    # 创建主窗口
    win = QWidget()

    # 创建4个QLabel控件
    l1 = QLabel()
    l2 = QLabel()
    l3 = QLabel()
    l4 = QLabel()

    # 设置各个Label的内容
    l1.setText("Hello World")  # 普通文本
    l2.setText("welcome to Python GUI Programming")  # 普通文本
    l3.setPixmap(QPixmap("python.jpg"))  # 显示图片
    l4.setText('<a href="https://www.tutorialspoint.com">TutorialsPoint</a>')  # 超链接文本

    # 设置文本对齐方式
    l1.setAlignment(Qt.AlignCenter)  # 居中对齐
    l3.setAlignment(Qt.AlignCenter)  # 居中对齐
    l4.setAlignment(Qt.AlignRight)  # 右对齐

    # 创建垂直布局并添加控件
    vbox = QVBoxLayout()
    vbox.addWidget(l1)  # 添加第一个Label
    vbox.addStretch()  # 添加伸缩空间
    vbox.addWidget(l2)  # 添加第二个Label
    vbox.addStretch()  # 添加伸缩空间
    vbox.addWidget(l3)  # 添加第三个Label(图片)
    vbox.addStretch()  # 添加伸缩空间
    vbox.addWidget(l4)  # 添加第四个Label(超链接)

    # 启用超链接点击功能
    l4.setOpenExternalLinks(True)

    # 设置主窗口布局并显示
    win.setLayout(vbox)
    win.setWindowTitle("QLabel Demo")
    win.show()
    # 启动应用事件循环
    sys.exit(app.exec_())

if __name__ == '__main__':
    window()
