import csv
import pydantic
from typing import List
from fastapi import APIRouter, Body, Depends
from ..utils.record import LOG_DIR
from ..utils.code_table import get_table, CodeTable
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


class GetRecordReq(pydantic.BaseModel):
    records: List[str] = []


def get_keys(req: GetRecordReq):
    paths = [LOG_DIR.joinpath(record) for record in req.records]
    paths.sort(key=lambda path: path.stat().st_mtime)
    data = []
    table = get_table()
    ret = []
    for path in paths:
        with path.open('r', encoding='utf8') as f:
            reader = csv.reader(f)
            keys = [row[1].strip() for row in reader]
            ret.append((path.name, keys))
    return ret


@api.post("/get_article")
async def get_article(name_keys=Depends(get_keys), table: CodeTable = Depends(get_table)):
    data = []
    for name, keys in name_keys:
        data.extend([word.json() for word in table.convert_article(keys)])
    return {'data': data}


@api.post("/get_optim")
async def get_optim(name_keys=Depends(get_keys), table: CodeTable = Depends(get_table)):
    data = []
    for name, keys in name_keys:
        article = table.convert_article(keys)
        for row in table.optim_article(article):
            data.append({
                "old": [word.json() for word in row[0]],
                "new": [word.json() for word in row[1]]
            })
    return {'data': data}
