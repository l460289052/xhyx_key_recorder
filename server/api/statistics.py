import csv
from collections import defaultdict

from fastapi import APIRouter

from ..record import LOG_DIR

api = APIRouter()


@api.get("/")
def get_info():
    data = defaultdict(int)
    with open(LOG_DIR.joinpath('record.log')) as f:
        reader = csv.reader(f)
        for row in reader:
            data[row[1]] += 1
    data = list(data.items())
    data.sort(key=lambda item: item[1], reverse=True)
    data = [{"word": item[0], "count":item[1]} for item in data]
    return {"data": data}
