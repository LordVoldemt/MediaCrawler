
import sys

from PyQt5.QtCore import *

from PyQt5.QtGui import *

from PyQt5.QtWidgets import *


# QSpinBox对象向用户显示一个文本框，该文本框在其右侧显示一个带有向上/向下按钮的整数。如果按下向上/向下按钮，文本框中的值会增加/减少。
# 默认情况下，框中的整数从 0 开始，到 99 并按步骤 1 更改。将 QDoubleSpinBox 用于浮点值
class spindemo(QWidget):
    """演示QSpinBox使用的自定义窗口类"""

    def __init__(self, parent=None):
        """初始化数字调节框演示窗口"""
        super(spindemo, self).__init__(parent)  # 调用父类构造函数

        # 创建垂直布局
        layout = QVBoxLayout()

        # 创建显示当前值的标签
        self.l1 = QLabel("current value:")
        self.l1.setAlignment(Qt.AlignCenter)  # 设置文本居中对齐
        layout.addWidget(self.l1)  # 添加到布局

        # 创建数字调节框
        self.sp = QSpinBox()
        layout.addWidget(self.sp)  # 添加到布局

        # 连接值变化信号到处理函数
        self.sp.valueChanged.connect(self.valuechange)

        # 设置窗口布局和标题
        self.setLayout(layout)
        self.setWindowTitle("SpinBox demo")

    def valuechange(self):
        """数值变化处理函数"""
        # 更新标签显示当前数值
        self.l1.setText("current value: " + str(self.sp.value()))



def main():

    app = QApplication(sys.argv)

    ex = spindemo()

    ex.show()

    sys.exit(app.exec_())



if __name__ == '__main__':

    main()

