import pathlib
import pytest
import csv
from ..code_table import get_table, InputWord


@pytest.fixture
def record_csv_keys():
    keys = []
    with pathlib.Path(__file__).parent.joinpath('record-for-test.log').open('r') as f:
        reader = csv.reader(f)
        for row in reader:
            keys.append(row[1].strip())
    return keys


def test_table():
    table = get_table()
    words = table.match_exact_code('kkll', 100, False)
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


def test_simple_convert():
    table = get_table()
    dic = {
        ' ': 'space'
    }
    article = 'v u yidrceuiigxu,t;yg keyipc ts;b;'
    article = [dic.get(key, key) for key in article]
    result = table.convert_article(article)
    result = ''.join(res.word for res in result)
    assert result == '这是一段测试程序,它应该可以跑通吧'


def test_log_convert(record_csv_keys):
    table = get_table()
    result = table.convert_article(record_csv_keys)
    result = ''.join(res.word for res in result)
    assert result == '运行状态 搜索码表 按键统计  分析 加载个人及系统配置文件用了673毫秒enter故意输错:其实根本没有错的啦'


def test_optim():
    table = get_table()
    keys = 'vs hx;r mb gs h gok '
    dic = {' ': 'space'}
    keys = [dic.get(key, key) for key in keys]
    article = list(table.convert_article(keys))
    words = ''.join(art.word for art in article)
    assert words == "中华人民共和国"
    optimed = list(table.optim_article(article))
    assert len(optimed) == 1
    assert ''.join(word.word for word in optimed[0][0]) == "中华人民共和国"
    assert optimed[0][1][0].code == 'vhrg'

    optimed = list(table.optim_article([InputWord('keng', '可能', '')]))
    assert len(optimed) == 1
    new_word = optimed[0][1][0]
    assert new_word.code == 'kn'
    assert new_word.committer == '1'


def test_optim_log(record_csv_keys):
    table = get_table()
    optimed = list(table.optim_article(table.convert_article(record_csv_keys)))
    assert len(optimed) > 0
