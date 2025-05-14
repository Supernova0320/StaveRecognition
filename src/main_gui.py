import sys
import threading
import os
import shutil
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QFileDialog
)
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon
from PyQt5.QtCore import Qt, pyqtSignal, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
import webbrowser  # 用于打开本地HTML文件

import recognition_client as rec
import player_engine


class MidiPlayerGUI(QWidget):
    recognition_done = pyqtSignal(str)
    recognition_failed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("五线谱识别播放系统")
        self.setFixedSize(1080, 720)
        self.set_ui_palette()
        self.setWindowIcon(QIcon('./resources/music.svg'))  # 加载窗口图标

        self.img_path = None
        self.mid_path = None

        self.init_ui()
        self.apply_styles()

        self.recognition_done.connect(self.display_html)
        self.recognition_failed.connect(self.display_recognition_error)

    def set_ui_palette(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#2D2D2D"))
        self.setPalette(palette)

    def init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # 左侧 WebView 容器（用于加载 HTML）
        self.web_view = QWebEngineView()
        self.web_view.setFixedSize(800, 650)
        self.web_view.setStyleSheet("""
            background-color: #1E1E1E;
            border: 1px solid #444;
            overflow: hidden;
        """)
        main_layout.addWidget(self.web_view)

        # 初始提示：识别未完成
        self.web_view.setHtml("""
            <html>
                <body style="background-color: #1E1E1E; color: #888; 
                             display: flex; justify-content: center; align-items: center;
                             height: 100%; font-size: 16px; font-family: 'Segoe UI'; margin: 0; padding: 0;">
                    识别未完成
                </body>
            </html>
        """)

        # 右侧操作面板
        right_panel_widget = QWidget()
        right_panel_widget.setFixedWidth(220)
        right_panel = QVBoxLayout(right_panel_widget)
        right_panel.setSpacing(20)

        title = QLabel("操作面板")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #CCCCCC;")
        right_panel.addWidget(title)

        self.load_button = QPushButton("导入图片")
        self.load_button.clicked.connect(self.load_file)
        right_panel.addWidget(self.load_button)

        self.recognize_button = QPushButton("开始识别")
        self.recognize_button.clicked.connect(self.recognition_entrance)
        right_panel.addWidget(self.recognize_button)

        self.state_text = QLabel("请先导入五线谱图片")
        self.state_text.setAlignment(Qt.AlignCenter)
        self.state_text.setStyleSheet("color: #AAAAAA;")
        right_panel.addWidget(self.state_text)

        self.view_score_button = QPushButton("查看乐谱")
        self.view_score_button.clicked.connect(self.view_score)
        right_panel.addWidget(self.view_score_button)

        self.play_button = QPushButton("播放并可视化")
        self.play_button.clicked.connect(self.play_entrance)
        right_panel.addWidget(self.play_button)

        self.play_text = QLabel("请先识别以生成 MIDI 文件")
        self.play_text.setAlignment(Qt.AlignCenter)
        self.play_text.setStyleSheet("color: #AAAAAA;")
        right_panel.addWidget(self.play_text)

        right_panel.addStretch()
        main_layout.addWidget(right_panel_widget)

        self.setLayout(main_layout)

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #2D2D2D;
            }
            QPushButton {
                background-color: #4A4A4A;
                color: #FFFFFF;
                border: 2px solid #5A5A5A;
                border-radius: 4px;
                padding: 10px 24px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #5A5A5A;
                border-color: #6A6A6A;
            }
            QLabel {
                color: #CCCCCC;
                font-size: 14px;
            }
        """)

    def load_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "PNG 文件 (*.png)")
        if path:
            self.img_path = path
            filename = os.path.basename(path)
            self.state_text.setText(f"已加载: {filename}")
            self.state_text.setStyleSheet("color: #66BB6A;")

            # 重置 WebView
            self.web_view.setHtml("""
                <html>
                    <body style="background-color: #1E1E1E; color: #888; 
                                 display: flex; justify-content: center; align-items: center;
                                 height: 100%; font-size: 18px; font-family: 'Segoe UI'; margin: 0; padding: 0;">
                        识别未完成
                    </body>
                </html>
            """)

    def recognition_entrance(self):
        if self.img_path:
            self.state_text.setText("识别中，请稍候...")
            self.state_text.setStyleSheet("color: #29B6F6;")
            thread = threading.Thread(target=self.start_rec)
            thread.daemon = True
            thread.start()
        else:
            self.state_text.setText("请先导入图片")
            self.state_text.setStyleSheet("color: #EF5350;")

    def start_rec(self):
        try:
            rec.run_recognition(self.img_path)
            html_path = os.path.abspath("midi_file/result.html")
            if os.path.exists(html_path):
                self.recognition_done.emit(html_path)
            else:
                self.recognition_failed.emit("HTML 文件未找到")
        except Exception as e:
            self.recognition_failed.emit(str(e))

    def display_html(self, html_path):
        self.state_text.setText("识别完成")
        self.state_text.setStyleSheet("color: #66BB6A;")
        self.web_view.load(QUrl.fromLocalFile(html_path))
        print(f"HTML 加载完成: {html_path}")

    def display_recognition_error(self, msg):
        self.state_text.setText(f"识别失败: {msg}")
        self.state_text.setStyleSheet("color: #EF5350;")

    def play_entrance(self):
        self.mid_path = os.path.abspath("midi_file/temp.mid")
        if not os.path.exists(self.mid_path):
            self.play_text.setText("MIDI 文件未找到，请先识别")
            self.play_text.setStyleSheet("color: #EF5350;")
            return
        thread = threading.Thread(target=self.start_play)
        thread.daemon = True
        thread.start()

    def start_play(self):
        try:
            player_engine.start_visual(self.mid_path)
        except Exception as e:
            print(f"播放错误: {e}")

    def view_score(self):
        # 打开本地 HTML 文件
        html_path = os.path.abspath("midi_file/result.html")
        if os.path.exists(html_path):
            webbrowser.open(f"file://{html_path}")  # 使用默认浏览器打开文件
        else:
            self.state_text.setText("乐谱文件未生成")
            self.state_text.setStyleSheet("color: #EF5350;")

    def closeEvent(self, event):
        target_dir = os.path.abspath("midi_file")
        try:
            if os.path.exists(target_dir):
                for filename in os.listdir(target_dir):
                    file_path = os.path.join(target_dir, filename)
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
            print("已清空 MIDI 文件夹")
        except Exception as e:
            print(f"关闭时清理失败: {e}")
        event.accept()


def run_gui():
    app = QApplication(sys.argv)
    window = MidiPlayerGUI()
    window.show()
    sys.exit(app.exec_())
