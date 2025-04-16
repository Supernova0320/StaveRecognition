import os
import time
import tkinter as tk
from tkinter import ttk, filedialog
from pygame import mixer


class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("MIDI 播放器")

        # 初始化混音器
        mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
        mixer.music.set_volume(0.5)

        # 界面元素
        self.create_widgets()
        self.playing = False
        self.paused = False
        self.current_file = ""
        self.song_length = 0
        self.update_interval = 500  # 界面刷新间隔（毫秒）

    def create_widgets(self):
        # 控制按钮区域
        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.pack(fill=tk.X)

        self.play_btn = ttk.Button(control_frame, text="播放", command=self.toggle_play)
        self.play_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = ttk.Button(control_frame, text="停止", command=self.stop)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        ttk.Button(control_frame, text="选择文件", command=self.open_file).pack(side=tk.LEFT, padx=5)

        # 音量控制
        volume_frame = ttk.Frame(self.root, padding=10)
        volume_frame.pack(fill=tk.X)

        ttk.Label(volume_frame, text="音量:").pack(side=tk.LEFT)
        self.volume = ttk.Scale(volume_frame, from_=0, to=1,
                                command=lambda v: mixer.music.set_volume(float(v)))
        self.volume.set(0.5)
        self.volume.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # 进度条
        self.progress = ttk.Progressbar(self.root, mode='determinate')
        self.progress.pack(fill=tk.X, padx=10, pady=5)

        # 时间显示
        self.time_label = ttk.Label(self.root, text="00:00 / 00:00")
        self.time_label.pack(pady=5)

        # 状态栏
        self.status = ttk.Label(self.root, text="就绪", relief=tk.SUNKEN)
        self.status.pack(fill=tk.X)

    def open_file(self):
        filetypes = [('音频文件', '*.mid')]
        filepath = filedialog.askopenfilename(filetypes=filetypes)
        if filepath:
            self.load_file(filepath)

    def load_file(self, filepath):
        try:
            mixer.music.load(filepath)
            self.current_file = filepath
            self.song_length = mixer.Sound(filepath).get_length()
            self.status.config(text=f"已加载: {os.path.basename(filepath)}")
            self.update_time_display(0, self.song_length)
            self.progress["maximum"] = self.song_length
        except Exception as e:
            self.status.config(text=f"错误: {str(e)}")

    def toggle_play(self):
        if not self.playing:
            if self.current_file:
                self.play()
            else:
                self.status.config(text="请先选择音频文件")
        else:
            self.pause()

    def play(self):
        if not self.playing:
            mixer.music.play()
            self.playing = True
            self.play_btn.config(text="暂停")
            self.root.after(self.update_interval, self.update_display)
        elif self.paused:
            mixer.music.unpause()
            self.paused = False
            self.play_btn.config(text="暂停")

    def pause(self):
        if self.playing and not self.paused:
            mixer.music.pause()
            self.paused = True
            self.play_btn.config(text="继续")

    def stop(self):
        mixer.music.stop()
        self.playing = False
        self.paused = False
        self.play_btn.config(text="播放")
        self.progress["value"] = 0
        self.update_time_display(0, self.song_length)

    def update_display(self):
        if self.playing and not self.paused:
            current_time = mixer.music.get_pos() / 1000  # 转换为秒
            self.progress["value"] = current_time
            self.update_time_display(current_time, self.song_length)

            if current_time < self.song_length:
                self.root.after(self.update_interval, self.update_display)
            else:
                self.stop()

    def update_time_display(self, current, total):
        def format_time(seconds):
            return time.strftime("%M:%S", time.gmtime(seconds))

        self.time_label.config(
            text=f"{format_time(current)} / {format_time(total)}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x800")
    player = MusicPlayer(root)
    root.mainloop()