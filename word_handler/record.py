import logging
import pathlib
from datetime import datetime
from multiprocessing import Queue

import keyboard

from .get_win import is_chinese


hotkeys = {'ctrl', 'alt'}
pressed_hotkeys = set()

queue = Queue()


def record(e: keyboard.KeyboardEvent):
    if not is_chinese():
        return pressed_hotkeys.clear()

    if e.name in hotkeys:
        if e.event_type == keyboard.KEY_DOWN:
            pressed_hotkeys.add(e.name)
        else:
            pressed_hotkeys.remove(e.name)
        return

    if e.event_type == keyboard.KEY_UP or pressed_hotkeys:
        return

    time = e.time
    if isinstance(time, float):
        time = datetime.fromtimestamp(time)
    queue.put(e.name)