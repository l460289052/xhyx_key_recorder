from ..db import get_db


def test_get_db():
    db = get_db(":memory:")
