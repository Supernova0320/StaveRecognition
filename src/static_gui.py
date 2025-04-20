import cv2
import sdl2.ext
import os
import mido
import numpy as np

from configs import *
from collections import deque


class StaticGUI:
    def __init__(self):
        self.piano_img_path = r"F:/Graduation Design/StaveRecognition/resources/piano.png"
        self.screen_x, self.screen_y = 1280, 720
        self.piano_x, self.piano_y = 1020, 109
        self.play_line = 519  # 以下是钢琴，碰到这里就表示正在播放
        self.future_time = 3  # 提前绘制3tick的音符
        self.image_base = None  # 要载入的图片对象
        self.pos_list = []  # 88个琴键，每个琴键的坐标范围
        self.window = None
        self.window_arr = None

        self.image_base = cv2.imread(self.piano_img_path, cv2.IMREAD_UNCHANGED)
        self.pos_list = self.get_note_pos(self.image_base[:, :, 0])
        sdl2.ext.init()
        self.window = sdl2.ext.Window("五线谱识别播放器", size=(self.screen_x, self.screen_y))
        self.window_arr = sdl2.ext.pixels3d(self.window.get_surface())  # 将window转化为一个像素组，每个像素都能操作RGBA
        self.window.show()

    # 找到每个按键的坐标位置
    def get_note_pos(self, image):
        last_color = BLACK
        for y in range(0, image.shape[1]):
            cur_color = image[self.play_line][y]
            if np.all(cur_color != WHITE) and np.all(cur_color != BLACK):  # 碰到了分界线
                last_color = cur_color
            elif np.all(last_color != cur_color):  # 和上一个颜色不一样，说明到了新的键
                self.pos_list.append(self.find_edge(image, cur_color, y))
                last_color = cur_color
        return self.pos_list

    # 找到每个按键的边缘
    def find_edge(self, image, cur_color, start_x):
        """
        用BFS找每个琴键的轮廓坐标
        """
        h, w = image.shape[:2]
        visited = set()
        queue = deque()
        mask = np.zeros((h, w), dtype=np.uint8)

        queue.append((start_x, self.play_line))
        visited.add((start_x, self.play_line))

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            x, y = queue.popleft()
            mask[y, x] = 255  # 标记为白

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h:
                    if (nx, ny) not in visited and np.all(image[ny][nx] == cur_color):
                        queue.append((nx, ny))
                        visited.add((nx, ny))
        # 找轮廓
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        for cnt in contours:
            if cv2.pointPolygonTest(cnt, (start_x, self.play_line), False) >= 0:
                return [tuple(pt[0]) for pt in cnt]

        return []
