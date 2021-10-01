import pathlib

import fastapi
from fastapi.staticfiles import StaticFiles

from .api import api_router


app = fastapi.FastAPI()

path = pathlib.Path(__file__).parent
app.mount("/static", StaticFiles(directory=path.joinpath("static").joinpath("static")), name="static")
app.mount("/page", StaticFiles(directory=path.joinpath("static"),
          html=True), "index.html")

app.include_router(api_router)


@app.get("/")
def index():
    return fastapi.responses.RedirectResponse("/page")
