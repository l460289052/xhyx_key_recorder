from ..code_table import get_table


def test_table():
    table = get_table()
    words = table.match_exact_code('kkll',100, False)
    assert words[0].word == '可可怜怜'

    words = table.match_exact_code('obb', 100, False)
    words = [word.word for word in words]
    assert words == [
        '冖',
        '宀',
        '丷',
        '疒',
        '勹',
        '比左部']
