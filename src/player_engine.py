import threading

import mido
import time
import keyboard as kb
import pretreatment
import dynamic_gui
import sdl2.ext

from static_gui import StaticGUI


def set_new_index(gui, partition, i, x, y, length, change, notes, port, paused):
    if gui.screen_y - 25 <= y <= gui.screen_y:
        target_time = length * x / gui.screen_x
        l = 0
        while partition[l]:
            if partition[l]["start_time"] > target_time:
                change += partition[l]["start_time"] - partition[i]["start_time"]
                for note in notes:
                    shut_msg = mido.Message(
                        "note_off",
                        note=note.note_id + 21,
                        channel=0,
                        velocity=0,
                        time=0,
                    )
                    port.send(shut_msg)
                    note.play_until = 0
                return change, l, paused
            l += 1
    return change, i, paused


def get_events(gui, p_mid, i, length, change, notes, port, paused):
    events = sdl2.ext.get_events()
    for e in events:
        # 暂停
        if e.type == sdl2.SDL_KEYDOWN:
            if e.key.keysym.sym == ord(" "):
                paused = not paused
        if e.type == sdl2.SDL_MOUSEBUTTONDOWN:
            change, i, paused = set_new_index(
                gui, p_mid, i, e.button.x, e.button.y, length, change, notes, port, paused
            )
    return change, i, paused


def create_thread(f, *args):
    t = f(*args)
    t.daemon = True
    t.start()
    return t


def play_loop(p_mid, port, gui, kb_notes, t):
    length = p_mid[-2]["start_time"]
    i = 0
    change = 0
    play_start = time.time()
    paused = False
    while p_mid[i]:
        t_cur = time.time()
        if not paused:
            for note in kb_notes:
                note.is_playing = t_cur < note.play_until
        # 接收事件
        change, i, paused = get_events(gui, p_mid, i, length, change, kb_notes, port, paused)
        t.future_part = pretreatment.get_future_part(p_mid, i, gui.future_time)
        t.time_code = t_cur + change - play_start
        if (t_cur + change - play_start) > p_mid[i]["start_time"]:
            if p_mid[i]["msg"].type == "note_on" and not p_mid[i]["msg"].velocity == 0:
                kb_notes[p_mid[i]["msg"].note - 21].play_until = t_cur + p_mid[i]["note_length"]
                kb_notes[p_mid[i]["msg"].note - 21].velocity = p_mid[i]["note_length"]
            if port:
                port.send(p_mid[i]["msg"])
            i += 1
            continue
        wait_time = p_mid[i]["start_time"] + play_start - (t_cur + change)
        if wait_time > 0.01:
            time.sleep(0.01)
        if paused:
            change -= time.time() - t_cur


def start_visual(midi_path):
    port = mido.open_output(mido.get_output_names()[0])
    keyboard_notes = [kb.KeyboardNote(i) for i in range(88)]
    gui = StaticGUI()

    mid = mido.MidiFile(midi_path)
    processed_mid, length = pretreatment.treat(mid)

    t = create_thread(dynamic_gui.DynamicGUI, keyboard_notes, gui, length)

    play_loop(processed_mid, port, gui, keyboard_notes, t)

    t.terminate()
