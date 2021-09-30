import logging
import pathlib
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

import keyboard

from .get_language import is_chinese

LOG_DIR = pathlib.Path(__file__).absolute().parents[1].joinpath("logs")
handler = TimedRotatingFileHandler(LOG_DIR.joinpath("record.log"), "midnight")
handler.suffix = "%Y-%m-%d"
logger = logging.getLogger("key")
logger.addHandler(handler)
logger.setLevel(logging.INFO)

hotkeys = {'ctrl', 'alt'}
pressed_hotkeys = set()


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
    key_logger = logging.getLogger("key")
    key_logger.info(f"{time}, {e.name}")
