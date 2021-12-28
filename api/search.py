from fastapi import APIRouter
from ..word_handler import code_table

api = APIRouter()


@api.get('/search')
async def search(code: str):
    data = []
    if len(code):
        table = code_table.get_table()
        for word in table.match_exact_code(code, 100, len(code) <= 2):
            data.append(word.dict())
        for word in table.match_exact_word(code, 100, len(code)<2):
            data.append(word.dict())
    return {"data": data}
