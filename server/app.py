import fastapi
import csv
import keyboard
from .record import LOG_DIR, record


remove_handler = None


app = fastapi.FastAPI()


@app.get("/")
def get_info():
    ret = []
    with open(LOG_DIR.joinpath('record.log')) as f:
        reader = csv.reader(f)
        for row in reader:
            ret.append(str(row))
    return ret


@app.get("/start")
def start_hook():
    global remove_handler
    ret = "none"
    if remove_handler is None:
        remove_handler = keyboard.hook(record)
        ret = "added"
    return ret


@app.get("/stop")
def stop_hook():
    global remove_handler
    if remove_handler is not None:
        remove_handler()
        remove_handler = None
