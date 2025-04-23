import time
import numpy as np
import cv2
from threading import Thread
from configs import *


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
        self.white_color = SKY_BLUE
        self.black_color = BLUE

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
        # 画键盘上的音符
        for note in self.playing_notes:
            if note.is_playing:
                self.draw_kb_note(note)

        # 画正在下落的
        self.draw_fall_note(t_cur)

        # 画进度条
        self.draw_bar()

        # 显示时间
        timer = "{}:{:02d}/{}:{:02d}".format(
            int(self.time_code / 60),
            int(self.time_code % 60),
            int(self.length / 60),
            int(self.length % 60),
        )
        self.draw_time(timer, self.st_gui.piano_x - 130, 25, 1)

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
            color = self.white_color
        else:
            color = self.black_color
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
                    cur_color = self.white_color
                else:
                    width = 10
                    cur_color = self.black_color
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
                cur_color = self.white_color
            else:
                width = 10
                cur_color = self.black_color
            height = duration / self.st_gui.future_time * (self.st_gui.play_line - 1)
            y_pos = self.st_gui.play_line - 1
            self.draw_rect(kb_pos, y_pos - height, kb_pos + width, y_pos, cur_color)

    def draw_bar(self):
        """
        画进度条
        """
        width = self.time_code / self.length * self.st_gui.piano_x
        self.draw_rect(0, self.st_gui.play_line + self.st_gui.piano_y + 1, width,
                       self.st_gui.play_line + self.st_gui.piano_y + 16, SPRING_GREEN)

    def draw_rect(self, x1, y1, x2, y2, color):
        pt1 = (x1, y1)
        pt2 = (x1, y2)
        pt3 = (x2, y2)
        pt4 = (x2, y1)
        pts = np.array([pt1, pt2, pt3, pt4], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.fillPoly(self.image, [pts], color)

    def draw_time(self, timer, x, y, alpha):
        font = cv2.FONT_ITALIC
        overlay = self.image.copy()
        cv2.putText(overlay, timer, (x, y), font, 0.75, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.addWeighted(overlay, alpha, self.image, 1 - alpha, 0, self.image)

    def terminate(self):
        self.running = False
