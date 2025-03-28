import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()  # 调用父类QWidget的初始化方法
        self.initUI()  # 调用界面初始化方法


    def initUI(self):
        # 创建水平布局
        hbox = QHBoxLayout(self)

        # 创建两个QFrame作为容器
        topleft = QFrame()
        topleft.setFrameShape(QFrame.StyledPanel)  # 设置框架样式
        bottom = QFrame()
        bottom.setFrameShape(QFrame.StyledPanel)

        # 创建水平分割器，添加左侧框架和文本编辑器
        splitter1 = QSplitter(Qt.Horizontal)
        textedit = QTextEdit()  # 创建文本编辑部件
        splitter1.addWidget(topleft)
        splitter1.addWidget(textedit)
        splitter1.setSizes([100, 200])  # 设置初始分割比例

        # 创建垂直分割器，将水平分割器和底部框架组合
        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(bottom)

        # 将垂直分割器添加到主布局
        hbox.addWidget(splitter2)

        self.setLayout(hbox)  # 设置主窗口布局
        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))  # 设置应用样式

        # 设置窗口位置、大小和标题
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QSplitter demo')
        self.show()  # 显示窗口


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
