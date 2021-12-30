from datetime import datetime
from multiprocessing import Queue

import keyboard

from .get_win import is_chinese


hotkeys = {'ctrl', 'alt'}
pressed_hotkeys = set()

queue = Queue()

last_key = None


def record(e: keyboard.KeyboardEvent):
    global last_key
    try:
        if e.event_type == keyboard.KEY_DOWN:
            if last_key == e.name == "ctrl":
                queue.put("-MOVE-")
            last_key = e.name
        # if not is_chinese():
        #     return pressed_hotkeys.clear()

        if e.name in hotkeys:
            if e.event_type == keyboard.KEY_DOWN:
                pressed_hotkeys.add(e.name)
            elif e.name in pressed_hotkeys:
                pressed_hotkeys.remove(e.name)
            return

        if e.event_type == keyboard.KEY_UP or pressed_hotkeys:
            return

        queue.put(e.name)
        if not is_chinese():
            queue.put("enter")
    except Exception as e:
        import logging
        logging.getLogger("exception").exception(e)
