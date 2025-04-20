import tkinter
import threading

import sys
sys.path.append('..')
import 


from tkinter import ttk, filedialog


class MidiPlayerRoot:
    def __init__(self, root):
        # 界面属性
        self.root = root
        self.root.title("🎵 五线谱识别播放系统")
        self.root.geometry("400x250")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        # 文件路径
        self.img_path = None

        # 内容属性
        self.title_label = None  # 标题
        self.load_button = None  # 加载按钮
        self.state_text = None  # 加载状态
        self.play_button = None  # 播放按钮
        self.recognize_button = None  # 识别按钮

        self.create_buttons()

    def create_buttons(self):
        style = ttk.Style()
        style.configure("TButton", font=("黑体", 12), padding=10)
        style.configure("TLabel", font=("黑体", 11))

        self.title_label = ttk.Label(self.root, text="五线谱图片识别", font=("黑体", 16, "bold"))
        self.title_label.pack(pady=(20, 10))

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=5)

        self.load_button = ttk.Button(button_frame, text="导入图片", command=self.load_file)
        self.load_button.grid(row=0, column=0, padx=10)

        self.recognize_button = ttk.Button(button_frame, text="开始识别", command=self.start_recognition)
        self.recognize_button.grid(row=0, column=1, padx=10)

        # 状态标签
        self.state_text = ttk.Label(self.root, text="未导入图片", foreground="gray")
        self.state_text.pack(pady=5)

        # 可视化按钮
        self.play_button = ttk.Button(self.root, text="进入可视化界面", command=self.start_playing)
        self.play_button.pack(pady=15)

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("PNG 文件", "*.png")])
        if path:
            self.img_path = path
            filename = path.split("/")[-1]
            self.state_text.config(text=f"已加载图片: {filename}", foreground="green")

    def start_recognition(self):
        if self.img_path:
            print(f"开始识别: {self.img_path}")
            self.state_text.config(text="识别中...", foreground="blue")
            # TODO: 调用识别逻辑
        else:
            self.state_text.config(text="请先导入图片", foreground="red")

    def start_playing(self):
        print("进入可视化界面")
        # TODO: 调用可视化界面逻辑


def run_gui():
    root = tkinter.Tk()
    MidiPlayerRoot(root)
    root.mainloop()
