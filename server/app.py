import csv
import pathlib
from collections import defaultdict

import fastapi
import keyboard
from fastapi.staticfiles import StaticFiles

from .record import LOG_DIR, record

remove_handler = None


app = fastapi.FastAPI()

path = pathlib.Path(__file__).parent

app.mount("/static", StaticFiles(directory=path.joinpath("static").joinpath("static")), name="static")
app.mount("/page", StaticFiles(directory=path.joinpath("static"),
          html=True), "index.html")


@app.get("/")
def index():
    return fastapi.responses.RedirectResponse("/page")

# @app.get("/")
# def get_page():


@app.get("/api/hello")
def hello():
    return "hello"


@app.get("/api/statistics")
def get_info():
    print("123")
    data = defaultdict(int)
    with open(LOG_DIR.joinpath('record.log')) as f:
        reader = csv.reader(f)
        for row in reader:
            data[row[1]] += 1
    data = list(data.items())
    data.sort(key=lambda item: item[1], reverse=True)
    data = [{"word": item[0], "count":item[1]} for item in data]
    return {"data": data}
# def get_info():
#     ret = []
#     with open(LOG_DIR.joinpath('record.log')) as f:
#         reader = csv.reader(f)
#         for row in reader:
#             ret.append(str(row))
#     return ret


@app.get("/api/start")
def start_hook():
    global remove_handler
    ret = "none"
    if remove_handler is None:
        remove_handler = keyboard.hook(record)
        ret = "added"
    return ret


@app.get("/api/stop")
def stop_hook():
    global remove_handler
    if remove_handler is not None:
        remove_handler()
        remove_handler = None
