import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
                             QPushButton, QVBoxLayout, QWidget, QHeaderView, QMessageBox,
                             QInputDialog, QHBoxLayout)


class TableDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTableWidget增删改查示例")
        self.resize(600, 400)

        # 创建主控件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # 创建表格
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "姓名", "年龄", "操作"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 创建按钮
        btn_add = QPushButton("添加数据")
        btn_add.clicked.connect(self.add_data)

        # 添加控件到布局
        layout.addWidget(self.table)
        layout.addWidget(btn_add)
        central_widget.setLayout(layout)

        # 初始化一些测试数据
        self.init_data()

    def init_data(self):
        """初始化测试数据"""
        test_data = [
            {"id": 1, "name": "张三", "age": 25},
            {"id": 2, "name": "李四", "age": 30},
            {"id": 3, "name": "王五", "age": 28}
        ]

        for data in test_data:
            self.add_row(data)

    def add_row(self, data):
        """添加一行数据到表格"""
        row = self.table.rowCount()
        self.table.insertRow(row)

        # 添加数据列
        self.table.setItem(row, 0, QTableWidgetItem(str(data["id"])))
        self.table.setItem(row, 1, QTableWidgetItem(data["name"]))
        self.table.setItem(row, 2, QTableWidgetItem(str(data["age"])))

        # 添加操作按钮
        btn_layout = QHBoxLayout()
        btn_widget = QWidget()

        btn_edit = QPushButton("编辑")
        btn_edit.clicked.connect(lambda: self.edit_data(row))

        btn_delete = QPushButton("删除")
        btn_delete.clicked.connect(lambda: self.delete_data(row))

        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_delete)
        btn_widget.setLayout(btn_layout)

        self.table.setCellWidget(row, 3, btn_widget)

    def add_data(self):
        """添加新数据"""
        name, ok = QInputDialog.getText(self, "添加数据", "请输入姓名:")
        if not ok or not name:
            return

        age, ok = QInputDialog.getInt(self, "添加数据", "请输入年龄:", min=1)
        if not ok:
            return

        # 生成新ID
        new_id = 1
        if self.table.rowCount() > 0:
            last_id = int(self.table.item(self.table.rowCount() - 1, 0).text())
            new_id = last_id + 1

        self.add_row({"id": new_id, "name": name, "age": age})

    def edit_data(self, row):
        """编辑数据"""
        name_item = self.table.item(row, 1)
        age_item = self.table.item(row, 2)

        new_name, ok = QInputDialog.getText(
            self, "编辑数据", "请输入姓名:", text=name_item.text())
        if not ok or not new_name:
            return

        new_age, ok = QInputDialog.getInt(
            self, "编辑数据", "请输入年龄:", value=int(age_item.text()), min=1)
        if not ok:
            return

        # 更新数据
        name_item.setText(new_name)
        age_item.setText(str(new_age))

    def delete_data(self, row):
        """删除数据"""
        reply = QMessageBox.question(
            self, "确认删除", "确定要删除这行数据吗?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.table.removeRow(row)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TableDemo()
    window.show()
    sys.exit(app.exec_())