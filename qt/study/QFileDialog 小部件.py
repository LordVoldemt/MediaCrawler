import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class filedialogdemo(QWidget):
    def __init__(self, parent=None):
        super(filedialogdemo, self).__init__(parent)

        # 创建垂直布局
        layout = QVBoxLayout()
        # 创建按钮1 - 用于演示静态方法打开文件
        self.btn = QPushButton("QFileDialog static method demo")
        self.btn.clicked.connect(self.getfile)

        layout.addWidget(self.btn)
        # 创建标签用于显示图片
        self.le = QLabel("Hello")

        layout.addWidget(self.le)
        # 创建按钮2 - 用于演示对象方式打开文件
        self.btn1 = QPushButton("QFileDialog object")
        self.btn1.clicked.connect(self.getfiles)
        layout.addWidget(self.btn1)

        # 创建文本编辑框用于显示文件内容
        self.contents = QTextEdit()
        layout.addWidget(self.contents)
        self.setLayout(layout)
        self.setWindowTitle("File Dialog demo")

    def getfile(self):
        # 使用静态方法打开文件对话框，筛选jpg和gif图片
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            'c:\\', "Image files (*.jpeg *.gif)")
        # 在标签上显示选中的图片
        self.le.setPixmap(QPixmap(fname))

    def getfiles(self):
        # 创建文件对话框对象
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)  # 设置可以选择任何文件
        dlg.setFilter("Text files (*.txt)")  # 设置文件过滤器为文本文件

        if dlg.exec_():
            # 获取用户选择的文件
            filenames = dlg.selectedFiles()
            f = open(filenames[0], 'r')

            with f:
                # 读取文件内容并显示在文本编辑框中
                data = f.read()
                self.contents.setText(data)


def main():
    app = QApplication(sys.argv)
    ex = filedialogdemo()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
