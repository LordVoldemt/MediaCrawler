
import sys

from PyQt5.QtCore import *

from PyQt5.QtGui import *

from PyQt5.QtWidgets import *

# 三板斧：
# 1.创建布局，
# 2.创建控件，
# 3.将控件添加到布局中，

class combodemo(QWidget):
    """演示QComboBox使用的自定义窗口类"""

    def __init__(self, parent=None):
        """初始化下拉框演示窗口"""
        super(combodemo, self).__init__(parent)  # 调用父类构造函数

        # 创建水平布局
        layout = QHBoxLayout()

        # 创建下拉框控件
        self.cb = QComboBox()
        # 添加单个选项
        self.cb.addItem("C")
        self.cb.addItem("C++")
        # 批量添加多个选项
        self.cb.addItems(["Java", "C#", "Python"])
        # 连接选项变化信号到处理函数,每当当前索引由用户或以编程方式更改时
        self.cb.currentIndexChanged.connect(self.selectionchange)

        # 将下拉框添加到布局
        layout.addWidget(self.cb)
        # 设置窗口布局
        self.setLayout(layout)
        # 设置窗口标题
        self.setWindowTitle("combo box demo")

    def selectionchange(self, i):
        """下拉框选项变化处理函数"""
        print("Items in the list are :")
        # 遍历并打印所有选项
        for count in range(self.cb.count()):
            print(self.cb.itemText(count))
        # 打印当前选中项的索引和文本
        print("Current index", i, "selection changed ", self.cb.currentText())



def main():

    app = QApplication(sys.argv)

    ex = combodemo()

    ex.show()

    sys.exit(app.exec_())



if __name__ == '__main__':

    main()

