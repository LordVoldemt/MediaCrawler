import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class sliderdemo(QWidget):
    """演示QSlider滑块控件的自定义窗口类"""

    def __init__(self, parent=None):
        """初始化滑块演示窗口"""
        super(sliderdemo, self).__init__(parent)  # 调用父类构造函数

        # 创建垂直布局
        layout = QVBoxLayout()

        # 创建显示文本的标签
        self.l1 = QLabel("Hello")
        self.l1.setAlignment(Qt.AlignCenter)  # 设置文本居中对齐
        layout.addWidget(self.l1)  # 添加到布局

        # 创建水平滑块控件
        self.sl = QSlider(Qt.Horizontal)  # 水平方向滑块
        self.sl.setMinimum(10)  # 设置最小值
        self.sl.setMaximum(30)  # 设置最大值
        self.sl.setValue(20)  # 设置初始值
        self.sl.setTickPosition(QSlider.TicksBelow)  # 刻度线显示在下方
        self.sl.setTickInterval(5)  # 刻度间隔为5

        # 将滑块添加到布局并连接信号
        layout.addWidget(self.sl)
        self.sl.valueChanged.connect(self.valuechange)  # 连接值变化信号

        # 完成窗口设置
        self.setLayout(layout)  # 应用布局
        self.setWindowTitle("SpinBox demo")  # 设置窗口标题

    def valuechange(self):
        """滑块值变化处理函数"""
        size = self.sl.value()  # 获取当前滑块值
        self.l1.setFont(QFont("Arial", size))  # 根据滑块值改变标签字体大小


def main():
    app = QApplication(sys.argv)
    ex = sliderdemo()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
