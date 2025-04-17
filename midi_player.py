import pygame
from pygame import mixer
import time
import mido


class MIDIPlayer:
    def __init__(self, midi_path):
        self.midi_path = midi_path
        self.total_duration = 0
        self.is_playing = False
        self.is_paused = False
        self.start_time = 0
        self.pause_start = 0
        self.total_paused_duration = 0
        self._calculate_total_duration()
        self._mixer_init()

    def _calculate_total_duration(self):
        """计算MIDI文件总时长"""
        try:
            midi = mido.MidiFile(self.midi_path)
            self.total_duration = midi.length
        except Exception as e:
            print(f"Error loading MIDI file: {e}")
            self.total_duration = 0

    def _mixer_init(self):
        """初始化音频混音器"""
        freq = 44100
        bit_size = -16
        channels = 2
        buffer = 2048
        mixer.init(freq, bit_size, channels, buffer)
        mixer.music.set_volume(0.9)

    def play(self):
        """开始播放"""
        if self.is_playing:
            return
        try:
            mixer.music.load(self.midi_path)
            mixer.music.play()
            self.is_playing = True
            self.is_paused = False
            self.start_time = time.time()
            self.total_paused_duration = 0
        except pygame.error as e:
            print(f"Playback error: {e}")

    def pause(self):
        """暂停播放"""
        if not self.is_playing:
            return
        mixer.music.pause()
        self.pause_start = time.time()
        self.is_playing = False
        self.is_paused = True

    def resume(self):
        """恢复播放"""
        if not self.is_paused:
            return
        mixer.music.unpause()
        self.total_paused_duration += time.time() - self.pause_start
        self.is_playing = True
        self.is_paused = False

    def stop(self):
        """停止播放"""
        mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.start_time = 0
        self.total_paused_duration = 0

    def get_current_position(self):
        """获取当前播放位置（秒）"""
        if self.is_playing:
            return time.time() - self.start_time - self.total_paused_duration
        return 0

    def get_total_duration(self):
        """获取总时长（秒）"""
        return self.total_duration

    def is_music_busy(self):
        """检查是否正在播放"""
        return mixer.music.get_busy()
