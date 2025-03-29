import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QRadioButton, QLabel, QPushButton, \
    QButtonGroup


class Form(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 性别选择
        self.gender_label = QLabel("选择性别:")
        self.male_radio = QRadioButton("男")
        self.female_radio = QRadioButton("女")

        self.gender_group = QButtonGroup(self)
        self.gender_group.addButton(self.male_radio)
        self.gender_group.addButton(self.female_radio)

        gender_layout = QHBoxLayout()
        gender_layout.addWidget(self.male_radio)
        gender_layout.addWidget(self.female_radio)

        # 分数选择
        self.score_label = QLabel("选择分数:")
        self.score_10 = QRadioButton("10")
        self.score_20 = QRadioButton("20")
        self.score_30 = QRadioButton("30")

        self.score_group = QButtonGroup(self)
        self.score_group.addButton(self.score_10)
        self.score_group.addButton(self.score_20)
        self.score_group.addButton(self.score_30)

        score_layout = QHBoxLayout()
        score_layout.addWidget(self.score_10)
        score_layout.addWidget(self.score_20)
        score_layout.addWidget(self.score_30)

        # 提交按钮
        self.submit_button = QPushButton("提交")
        self.submit_button.clicked.connect(self.submit)

        # 布局
        layout.addWidget(self.gender_label)
        layout.addLayout(gender_layout)
        layout.addWidget(self.score_label)
        layout.addLayout(score_layout)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)
        self.setWindowTitle("表单示例")

    def submit(self):
        gender = "男" if self.male_radio.isChecked() else "女" if self.female_radio.isChecked() else "未选择"
        score = "未选择"
        for btn in [self.score_10, self.score_20, self.score_30]:
            if btn.isChecked():
                score = btn.text()
                break
        print(f"性别: {gender}, 分数: {score}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())
