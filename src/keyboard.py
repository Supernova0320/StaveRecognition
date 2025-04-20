import threading
import time

# 从A开始，True是白False是黑
BLACK_OR_WHITE = [True, False, True, True, False, True, False, True, True, False, True, False]


class KeyboardNote:
    def __init__(self, note_id):
        self.note_id = note_id
        self.play_until = 0
        self.velocity = 0
        self.is_playing = False
        self.is_white = BLACK_OR_WHITE[note_id % 12]
