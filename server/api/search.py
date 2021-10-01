from fastapi import APIRouter

api = APIRouter()


@api.get('/')
def search(code: str):
    return {"data":[{"code":1,"word":2,"file":3}]}
