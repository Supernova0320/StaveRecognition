import sys
import threading
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QFileDialog
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt

import recognition_client as rec
import player_engine


class MidiPlayerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("五线谱识别播放系统")
        self.setFixedSize(600, 420)
        self.set_ui_palette()

        self.img_path = None
        self.mid_path = None

        self.init_ui()

    def set_ui_palette(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#f8f9fa"))
        self.setPalette(palette)
        self.setStyleSheet("background-color: #f8f9fa;")

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(24)

        # 标题
        self.title_label = QLabel("五线谱识别播放")
        self.title_label.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: #333333;")
        main_layout.addWidget(self.title_label)

        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        self.load_button = QPushButton("导入图片")
        self.load_button.setFont(QFont("Segoe UI", 12))
        self.load_button.setStyleSheet(self.button_style("#4a90e2"))
        self.load_button.clicked.connect(self.load_file)

        self.recognize_button = QPushButton("开始识别")
        self.recognize_button.setFont(QFont("Segoe UI", 12))
        self.recognize_button.setStyleSheet(self.button_style("#0078d7"))
        self.recognize_button.clicked.connect(self.recognition_entrance)

        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.recognize_button)

        main_layout.addLayout(button_layout)

        # 状态标签
        self.state_text = QLabel("请导入五线谱图片")
        self.state_text.setFont(QFont("Segoe UI", 11))
        self.state_text.setStyleSheet("color: #666666;")
        self.state_text.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.state_text)

        # 可视化播放按钮
        self.play_button = QPushButton("播放并可视化")
        self.play_button.setFont(QFont("Segoe UI", 12))
        self.play_button.setStyleSheet(self.button_style("#28a745"))
        self.play_button.clicked.connect(self.play_entrance)
        main_layout.addWidget(self.play_button)

        # 播放状态标签
        self.play_text = QLabel("请先识别以生成 MIDI 文件")
        self.play_text.setFont(QFont("Segoe UI", 11))
        self.play_text.setStyleSheet("color: #666666;")
        self.play_text.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.play_text)

        self.setLayout(main_layout)

    def button_style(self, bg_color="#4a90e2"):
        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: white;
                padding: 10px 24px;
                border: none;
                border-radius: 6px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: #357ABD;
            }}
        """

    def load_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "PNG 文件 (*.png)")
        if path:
            self.img_path = path
            filename = os.path.basename(path)
            self.state_text.setText(f"已加载: {filename}")
            self.state_text.setStyleSheet("color: #2e8b57;")

    def recognition_entrance(self):
        if self.img_path:
            self.state_text.setText("识别中，请稍候...")
            self.state_text.setStyleSheet("color: #0078d7;")
            thread = threading.Thread(target=self.start_rec)
            thread.daemon = True
            thread.start()
        else:
            self.state_text.setText("请先导入图片")
            self.state_text.setStyleSheet("color: #d9534f;")

    def start_rec(self):
        try:
            rec.run_recognition(self.img_path)
            self.state_text.setText("识别完成")
            self.state_text.setStyleSheet("color: #28a745;")
        except Exception as e:
            self.state_text.setText(f"识别失败: {str(e)}")
            self.state_text.setStyleSheet("color: #d9534f;")

    def play_entrance(self):
        self.mid_path = "midi_file/temp.mid"
        if not os.path.exists(self.mid_path):
            self.play_text.setText("MIDI 文件未找到，请先识别")
            self.play_text.setStyleSheet("color: #d9534f;")
            return
        thread = threading.Thread(target=self.start_play)
        thread.daemon = True
        thread.start()

    def start_play(self):
        try:
            player_engine.start_visual(self.mid_path)
        except Exception as e:
            print(e)


def run_gui():
    app = QApplication(sys.argv)
    window = MidiPlayerGUI()
    window.show()
    sys.exit(app.exec_())
