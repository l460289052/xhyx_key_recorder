from fastapi import APIRouter
import keyboard
from ..utils.record import record
api = APIRouter(tags=['control'])

remove_handler = None


@api.post("/set_hook_state")
async def set_hook_state(running: bool):
    global remove_handler
    if running:
        ret = "none"
        if remove_handler is None:
            remove_handler = keyboard.hook(record)
            ret = "added"
        return ret
    else:
        if remove_handler is not None:
            remove_handler()
            remove_handler = None
        return "stopped"


@api.get("/get_hook_state")
async def get_hook_state():
    return {'running': remove_handler is not None}
