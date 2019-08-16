# -*- coding:utf-8 -*-
# !/usr/bin/env python3
import sys
import re
import js2py
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLineEdit, QVBoxLayout, QPushButton, QLabel, QDialog
from PyQt5 import QtGui
from PyQt5.Qt import Qt
from requests import Session


class MainPageCenter(QWidget):
    """
        Class main window
    """

    def __init__(self):
        super(MainPageCenter, self).__init__()
        self.setWindowTitle('刷微信运动步数')
        self.main_layout = QVBoxLayout()
        self.top_layout = QHBoxLayout()
        self.bottom_layout = QHBoxLayout()
        self.under_layout_1 = QHBoxLayout()
        self.under_layout_2 = QHBoxLayout()
        self.top_label = QLabel()
        self.bottom_label = QLabel()
        self.under_label = QLabel()
        self.top_input = QLineEdit(self)
        self.bottom_input = QLineEdit(self)
        self.btn = QPushButton(self)
        self.init_ui()
        self.init_event()

    def init_ui(self):
        self.setFixedSize(640, 360)
        self.top_input.setFixedSize(200, 50)
        self.top_input.setPlaceholderText('请输入已绑定微信的卓易账号')
        self.bottom_input.setPlaceholderText('请输入要修改的步数(1~98800)')
        self.bottom_input.setFixedSize(200, 50)
        self.btn.setFixedSize(260, 50)
        self.btn.setText('开始刷')
        self.btn.setCursor(Qt.PointingHandCursor)
        self.top_label.setText('卓易账号')
        self.bottom_label.setText('输入步数')
        self.top_label.setFixedSize(50, 50)
        self.bottom_label.setFixedSize(50, 50)

        self.top_layout.setContentsMargins(0, 0, 0, 20)
        self.top_layout.setAlignment(Qt.AlignCenter)
        self.top_layout.addWidget(self.top_label)
        self.top_layout.addSpacing(10)
        self.top_layout.addWidget(self.top_input)

        self.bottom_layout.setContentsMargins(0, 0, 0, 40)
        self.bottom_layout.setAlignment(Qt.AlignCenter)
        self.bottom_layout.addWidget(self.bottom_label)
        self.bottom_layout.addSpacing(10)
        self.bottom_layout.addWidget(self.bottom_input)

        self.under_layout_1.setAlignment(Qt.AlignCenter)
        self.under_layout_2.setAlignment(Qt.AlignCenter)
        self.under_label.setText("""
1、安装下载【卓易健康】APP,可在各大应用市场下载
2、苹果可在App Store或其他平台下载。安卓下载卓易健康app
3、安装APP并注册账号后点击-我-微信运动-绑定至相关微信设备即可.
4、绑定微信后，在本页面输入刚刚注册的账号及要修改的步数点击提交修改
5、建议每次递交步数间隔不得超过9000,如第一次8999,第二次17998以此类推。微信上限98800。
6、凌晨12点到2点关闭修改，选择其他时间修改。如果不会理解差请多看几遍，或询问Q群管理。
        """)
        self.under_label.setStyleSheet('color:red')
        # self.under_layout_1.addSpacing(70)
        self.under_layout_1.addWidget(self.btn)
        self.under_layout_2.addWidget(self.under_label)

        # self.main_layout.addWidget(self.top_input)
        # self.main_layout.addWidget(self.bottom_input)
        self.main_layout.addLayout(self.top_layout)
        # self.main_layout.addSpacing(20)
        self.main_layout.addLayout(self.bottom_layout)
        self.main_layout.addLayout(self.under_layout_1)
        self.main_layout.addLayout(self.under_layout_2)
        # self.main_layout.setContentsMargins(0, 0, 0, 0)
        # self.main_layout.setSpacing(1)
        self.setLayout(self.main_layout)
        self.setStyleSheet('background-color:#99CCCC')
        icon = QtGui.QIcon("weixin.png")
        self.setWindowIcon(icon)

    def submit_updates(self):
        if not self.top_input.text():
            print('top_input')
            text = '请输入卓易账号'
            msg = MessageBox(self, text)
            msg.show()
            return
        elif not self.bottom_input.text():
            print('bottom_input')
            text = '请输入微信步数'
            msg = MessageBox(self, text)
            msg.show()
            return
        post_url = 'http://tool.chaojingxuan.com/wxsport/sport.php?openid=%s&steps=%s&hashsalt=%s'
        url = 'http://tool.chaojingxuan.com/wxsport/'
        session = Session()
        text = session.get(url).text
        li = re.findall(r'var hashsalt = (.*?);\n</script>', text, re.S)
        hashsalt = js2py.eval_js(li[0])
        ret = session.get(post_url % (self.top_input.text(), self.bottom_input.text(), hashsalt)).json()
        msg = MessageBox(self, ret.get('message'))
        msg.show()

    def init_event(self):
        self.btn.clicked.connect(self.submit_updates)


class MessageBox(QWidget):
    STYLE_QSS = """
              QWidget{background-color:#313233; font-family:"Microsoft YaHei";border-radius:3px;}
              """

    def __init__(self, parent=None, prompt_message="正在生成审讯报告，请稍等"):
        super(MessageBox, self).__init__(parent)
        self.parent = parent
        self.prompt_message = prompt_message
        self.setFixedSize(640, 360)
        # self.setModal(True)
        self.label_tip = None
        self.main_layout = QVBoxLayout()
        self.body_layout = QVBoxLayout()
        self.head_widget = QWidget()
        self.body_widget = QWidget()
        self.confirm_btn = QPushButton()
        self.head_layout = QHBoxLayout()
        self.head_label = QLabel("系统提示")
        self.body_layout = QVBoxLayout()
        self.body_label_layout = QHBoxLayout()
        self.body_button_layout = QHBoxLayout()
        self.init_ui()
        self.setStyleSheet(self.STYLE_QSS)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(self.STYLE_QSS)

    def init_ui(self):
        label_qss = """QLabel {color: #000000; font-family:'Microsoft YaHei';background-color:transparent ;
                        font-size:16px;
                        }"""
        self.label_tip = QLabel(self.prompt_message)
        self.label_tip.setAlignment(Qt.AlignCenter)
        self.label_tip.setStyleSheet(label_qss)
        self.body_label_layout.addWidget(self.label_tip)
        self.body_button_layout.setContentsMargins(0, 0, 0, 0)
        self.body_button_layout.setSpacing(0)
        self.confirm_btn.setText('确认')
        self.confirm_btn.setStyleSheet('background-color:#66CCFF;font-size:20px;')
        self.confirm_btn.setFixedSize(150, 40)
        self.confirm_btn.setCursor(Qt.PointingHandCursor)
        self.confirm_btn.clicked.connect(self.closeEvent)
        self.body_button_layout.addWidget(self.confirm_btn)
        self.body_button_layout.setAlignment(Qt.AlignCenter)
        self.body_layout.addLayout(self.body_label_layout)
        self.body_layout.addSpacing(6)
        self.body_layout.addLayout(self.body_button_layout)
        self.body_layout.addSpacing(30)
        self.body_layout.setContentsMargins(0, 0, 0, 0)
        self.body_layout.setSpacing(0)
        self.body_widget.setStyleSheet("background-color:#99CCCC")
        self.body_widget.setLayout(self.body_layout)
        self.body_widget.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.body_widget)

        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)
        # self.setStyleSheet("background-color:#1c1c1c")

    def closeEvent(self, event):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainPageCenter()
    ex.show()
    sys.exit(app.exec())

