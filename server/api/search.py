from fastapi import APIRouter
from ..utils import code_table

api = APIRouter()


@api.get('/')
async def search(code: str):
    data = []
    if len(code):
        table = code_table.get_table()
        for word in table.match_exact_code(code, 100, len(code) <= 2):
            data.append({
                "code": word.code,
                "word": word.word,
                "file": word.file})
    return {"data": data}
