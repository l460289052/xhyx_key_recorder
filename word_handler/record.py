from multiprocessing import Queue
from typing import Any, List, Optional, Tuple, Union

import keyboard

from .get_win import is_chinese

hotkeys = {'ctrl', 'alt'}
pressed_hotkeys = set()

queue = Queue()


class StateMachine:
    def __init__(self) -> None:
        self.root = {}
        self.state = self.root

    def add_path(self, path: List[Tuple[Any]], key: str):  # 需要在这里建立失匹配函数了……
        current = self.root
        for p in path:
            assert p != "ret"
            current = current.setdefault(p, {})
        current["ret"] = key

    def match(self, event: Tuple[Any]) -> Optional[str]:
        self.state = self.state.get(event, self.root.get(event, self.root))
        return self.state.get("ret", None)


sm = StateMachine()
sm.add_path([("ctrl", keyboard.KEY_DOWN),
            ("ctrl", keyboard.KEY_UP)] * 2, "double ctrl")


def record(e: keyboard.KeyboardEvent):
    try:
        match sm.match((e.name, e.event_type)):
            case "double ctrl":
                queue.put("-MOVE-")

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
