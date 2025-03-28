import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *


class tab_demo(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(1500, 1000)  # 调整窗口大小
        self.setWindowTitle("小红书获客系统v1.00")

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.tabs.addTab(self.tab1, "关键词追踪任务")
        self.tabs.addTab(self.tab2, "帖子ID追踪任务")

        self.tab1UI()
        self.tab2UI()

    def tab1UI(self):
        layout = QVBoxLayout()

        # 添加按钮靠右展示
        self.add_button = QPushButton("添加")
        self.add_button.setFixedSize(50, 50)
        add_button_layout = QHBoxLayout()
        add_button_layout.addStretch()
        add_button_layout.addWidget(self.add_button)
        self.add_button.clicked.connect(self.open_form)
        layout.addLayout(add_button_layout)

        # 创建表格
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["城市", "关键词", "帖子排序", "分析评论", "状态", "操作"])
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)  # 表头左对齐
        layout.addWidget(self.table)

        self.tab1.setLayout(layout)

    def add_row(self, city, keyword, post_sort, analyze_comments, status):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        for col, value in enumerate([city, keyword, post_sort, analyze_comments, status]):
            item = QTableWidgetItem(value)
            item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # 左对齐
            self.table.setItem(row_position, col, item)

        # 添加操作按钮
        btn_layout = QHBoxLayout()

        # 创建按钮
        restart_btn = QPushButton("重启")
        pause_btn = QPushButton("暂停")
        edit_btn = QPushButton("编辑")
        delete_btn = QPushButton("删除")

        # 调整按钮大小
        for btn in [restart_btn, pause_btn, edit_btn, delete_btn]:
            btn.setFixedSize(50, 50)

        # 添加水平间隙
        btn_layout.addStretch()  # 左侧留空
        btn_layout.addWidget(restart_btn)
        btn_layout.addSpacing(10)  # 按钮之间的间隙
        btn_layout.addWidget(pause_btn)
        btn_layout.addSpacing(10)  # 按钮之间的间隙
        btn_layout.addWidget(edit_btn)
        btn_layout.addSpacing(10)  # 按钮之间的间隙
        btn_layout.addWidget(delete_btn)
        btn_layout.addStretch()  # 右侧留空

        # 绑定按钮事件
        edit_btn.clicked.connect(lambda: self.open_form(edit=True, row=row_position))
        delete_btn.clicked.connect(lambda: self.table.removeRow(row_position))

        # 将按钮布局放到表格单元格
        container = QWidget()
        container.setLayout(btn_layout)
        self.table.setCellWidget(row_position, 5, container)

    def open_form(self, edit=False, row=None):
        dialog = QDialog(self)
        dialog.setWindowTitle("添加/编辑任务")
        form_layout = QFormLayout()

        city_input = QLineEdit()
        keyword_input = QLineEdit()

        post_sort_layout = QHBoxLayout()
        latest_checkbox = QCheckBox("最新")
        hottest_checkbox = QCheckBox("最热")
        comprehensive_checkbox = QCheckBox("综合")
        post_sort_layout.addWidget(latest_checkbox)
        post_sort_layout.addWidget(hottest_checkbox)
        post_sort_layout.addWidget(comprehensive_checkbox)

        track_count_layout = QHBoxLayout()
        ten_checkbox = QCheckBox("10")
        twenty_checkbox = QCheckBox("20")
        thirty_checkbox = QCheckBox("30")
        track_count_layout.addWidget(ten_checkbox)
        track_count_layout.addWidget(twenty_checkbox)
        track_count_layout.addWidget(thirty_checkbox)

        analyze_comments_checkbox = QCheckBox("否")

        form_layout.addRow("城市", city_input)
        form_layout.addRow("关键词", keyword_input)
        form_layout.addRow("帖子排序", post_sort_layout)
        form_layout.addRow("跟踪帖子数量", track_count_layout)
        form_layout.addRow("是否分析评论", analyze_comments_checkbox)

        if edit and row is not None:
            city_input.setText(self.table.item(row, 0).text())
            keyword_input.setText(self.table.item(row, 1).text())

        save_button = QPushButton("保存")
        save_button.clicked.connect(
            lambda: self.save_form(dialog, city_input.text(), keyword_input.text(), "综合", "否", "运行中"))
        save_button.setFixedSize(50, 50)
        save_button_layout = QHBoxLayout()
        save_button_layout.addStretch()
        save_button_layout.addWidget(save_button)
        save_button_layout.addStretch()
        form_layout.addRow(save_button_layout)

        dialog.setLayout(form_layout)
        dialog.exec_()

    def save_form(self, dialog, city, keyword, post_sort, analyze_comments, status):
        self.add_row(city, keyword, post_sort, analyze_comments, status)
        dialog.accept()

    def tab2UI(self):
        layout = QFormLayout()
        self.tab2.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = tab_demo()
    ex.show()
    sys.exit(app.exec_())





