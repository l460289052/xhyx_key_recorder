import csv
import pydantic
from typing import List
from fastapi import APIRouter, Body
from ..utils.record import LOG_DIR
from ..utils.code_table import get_table
api = APIRouter()


@api.get("/get_records")
async def get_records():
    data = []
    for record in LOG_DIR.iterdir():
        if record.name.startswith('record.log'):
            data.append(record.name)
    return {
        "data": data
    }


class GetArticleReq(pydantic.BaseModel):
    records: List[str] = []


@api.post("/get_article")
def get_article(req: GetArticleReq):
    paths = [LOG_DIR.joinpath(record) for record in req.records]
    paths.sort(key=lambda path: path.stat().st_mtime)
    data = []
    table = get_table()
    for path in paths:
        with path.open('r', encoding='utf8') as f:
            reader = csv.reader(f)
            keys = [row[1].strip() for row in reader]
        data.extend([word.json() for word in table.convert_article(keys)])
    return {'data': data}
