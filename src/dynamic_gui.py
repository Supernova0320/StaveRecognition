import time
import numpy as np
import cv2
from threading import Thread
from configs import *
import static_gui


class DynamicGUI(Thread):
    def __init__(self, playing_notes, st_gui, length):
        Thread.__init__(self)
        self.image = None
        self.playing_notes = playing_notes  # 正在播放的音符列表
        self.st_gui = st_gui
        self.running = True  # 一旦实例化就开始运行
        self.time_code = 0
        self.length = length
        self.future_part = None  # 未来一段时间的音符列表

    def run(self):
        # 反复重画GUI
        while self.running:
            t_cur = time.time()
            self.draw_dynamic(t_cur)

    def draw_dynamic(self, t_cur):
        """
        重画此时的所有音符
        """
        self.image = self.st_gui.image_base.copy()
        for note in self.playing_notes:
            if note.is_playing:
                self.draw_kb_note(note)  # 画键盘上的音符
        # 画正在下落的
        self.draw_fall_note(t_cur)
        # 画进度条

        # 显示时间

        # 刷新页面
        self.image = cv2.resize(
            self.image, (self.st_gui.screen_x, self.st_gui.screen_y), interpolation=cv2.INTER_CUBIC
        )
        np.copyto(self.st_gui.window_arr, self.image.swapaxes(0, 1))
        self.st_gui.window.refresh()

    def draw_kb_note(self, note):
        """
        绘制琴键上的颜色
        """

        pts = np.array(self.st_gui.pos_list[note.note_id], np.int32)
        pts = pts.reshape(-1, 1, 2)
        if note.is_white:
            color = YELLOW
        else:
            color = BRIGHT_YELLOW
        cv2.fillPoly(self.image, [pts], color)
        cv2.polylines(self.image, [pts], True, BLACK)

    def draw_fall_note(self, t_cur):
        """
        绘制掉落中的音符
        """
        if not self.future_part:
            return
        # 绘制没碰到play_line的音符
        for note in self.future_part:
            if note["msg"].type == "note_on" and note["msg"].velocity > 0:
                kb_note = note["msg"].note - 21
                kb_pos = self.st_gui.pos_list[kb_note][0][0]
                if self.playing_notes[note["msg"].note - 21].is_white:
                    width = 16
                    cur_color = YELLOW
                else:
                    width = 10
                    cur_color = BRIGHT_YELLOW
                height = note["note_length"] / self.st_gui.future_time * self.st_gui.play_line
                t = note["start_time"] - self.time_code
                y_pos = t / self.st_gui.future_time * self.st_gui.play_line
                y_pos = self.st_gui.play_line - y_pos
                self.draw_rect(kb_pos, y_pos - height, kb_pos + width, y_pos, cur_color)
        # 绘制碰到play_line的音符
        for note in self.playing_notes:
            duration = note.play_until - t_cur
            if duration <= 0:
                continue
            kb_note = note.note_id
            kb_pos = self.st_gui.pos_list[kb_note][0][0]
            if note.is_white:
                width = 16
                cur_color = YELLOW
            else:
                width = 10
                cur_color = BRIGHT_YELLOW
            height = duration / self.st_gui.future_time * (self.st_gui.play_line - 1)
            y_pos = self.st_gui.play_line - 1
            self.draw_rect(kb_pos, y_pos - height, kb_pos + width, y_pos, cur_color)

    def draw_rect(self, x1, y1, x2, y2, color):
        pt1 = (x1, y1)
        pt2 = (x1, y2)
        pt3 = (x2, y2)
        pt4 = (x2, y1)
        pts = np.array([pt1, pt2, pt3, pt4], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.fillPoly(self.image, [pts], color)
        cv2.polylines(self.image, [pts], True, BLACK)

    def terminate(self):
        self.running = False
