import threading

import mido
import time
import keyboard as kb
import pretreatment
import dynamic_gui

from static_gui import StaticGUI
from dynamic_gui import DynamicGUI


def create_thread(f, *args):
    t = f(*args)
    t.daemon = True
    t.start()
    return t


def play_loop(p_mid, port, gui, kb_notes, t, speed):
    length = p_mid[-2]["start_time"]
    i = 0
    play_start = time.time()
    while p_mid[i]:
        t_cur = time.time()
        for note in kb_notes:
            note.is_playing = t_cur < note.play_until
        t.future_part = pretreatment.get_future_part(p_mid, i, gui.future_time)
        t.time_code = t_cur - play_start
        if (t_cur - play_start) * speed > p_mid[i]["start_time"]:
            if p_mid[i]["msg"].type == "note_on" and not p_mid[i]["msg"].velocity == 0:
                kb_notes[p_mid[i]["msg"].note - 21].play_until = t_cur + p_mid[i]["note_length"]
                kb_notes[p_mid[i]["msg"].note - 21].velocity = p_mid[i]["note_length"]
            if port:
                port.send(p_mid[i]["msg"])
            i += 1
            continue
        wait_time = p_mid[i]["start_time"] + play_start - t_cur
        if wait_time > 0.01:
            time.sleep(0.01)


def start_visual(midi_path):
    port = mido.open_output(mido.get_output_names()[0])
    keyboard_notes = [kb.KeyboardNote(i) for i in range(88)]
    gui = StaticGUI()

    mid = mido.MidiFile(midi_path)
    processed_mid, length = pretreatment.treat(mid)

    t = create_thread(dynamic_gui.DynamicGUI, keyboard_notes, gui, length)
    play_loop(processed_mid, port, gui, keyboard_notes, t, 1)
    t.terminate()
