import cv2
import sdl2.ext
import os
import mido
import numpy as np

from configs import *
from collections import deque


class DrawGUI:
    def __int__(self):
        self.piano_img_path = r"../resources/piano.png"
        self.screen_x, self.screen_y = 1280, 720
        self.piano_x, self.piano_y = 1020, 109
        self.play_line = 519  # 以下是钢琴，碰到这里就表示正在播放
        self.future_time = 3  # 提前绘制3tick的音符
        self.image_base = None  # 要载入的图片对象
        self.pos_list = None  # 88个琴键，每个琴键的坐标范围
        self.window = None
        self.window_arr = None

        self.image_base = cv2.imread(self.piano_img_path, cv2.IMREAD_UNCHANGED)
        self.pos_list = self.get_note_pos()
        sdl2.ext.init()
        self.window = sdl2.ext.Window("五线谱识别播放器", size=(self.screen_x, self.screen_y))
        self.window_arr = sdl2.ext.pixels3d(self.window.get_surface())  # 将window转化为一个像素组，每个像素都能操作RGBA
        self.window.show()

    # 找到每个按键的坐标位置
    def get_note_pos(self):
        last_color = BLACK
        for y in range(0, self.image_base.shape[1]):
            cur_color = self.image_base[self.play_line][y]
            if np.all(cur_color != WHITE) and np.all(cur_color != BLACK):  # 碰到了分界线
                last_color = cur_color
            elif np.all(last_color != cur_color):  # 和上一个颜色不一样，说明到了新的键
                self.pos_list.append(self.find_edge(cur_color, y))
                last_color = cur_color
        return self.pos_list

    # 找到每个按键的坐标范围
    def find_edge(self, cur_color, y):
        x = self.play_line
        height, width = self.image_base.shape[:2]
        visited = set()
        bfs_queue = deque()
        mask = np.zeros((height, width), dtype=np.uint8)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        bfs_queue.append((x, y))
        while bfs_queue:
            cur_x, cur_y = bfs_queue.popleft()
            visited.add((cur_x, cur_y))
            mask[x, y] = 255  # 内部点标记成白色

            for dx, dy in directions:
                next_x, next_y = cur_x + dx, cur_y + dy
                if 0 <= next_x < height and 0 <= y < width:
                    if (next_x, next_y) not in visited:
                        bfs_queue.append((next_x, next_y))

        # 找轮廓
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        for cnt in contours:
            if cv2.pointPolygonTest(cnt, (y, x), False) >= 0:
                return [tuple(pt[0]) for pt in cnt]

        return []
