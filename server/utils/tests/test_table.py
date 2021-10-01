import pathlib
import csv
from ..code_table import get_table


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
    article = 'v u;yidrceuiigxu,t;yg keyipc ts;b;'
    article = [dic.get(key, key) for key in article]
    result = table.convert_article(article)
    result = ''.join(res.word for res in result)
    assert result == '这时一段测试程序sign它应该可以跑通吧'


def test_log_convert():
    table = get_table()
    keys = []
    with pathlib.Path(__file__).parent.joinpath('record-for-test.log').open('r') as f:
        reader = csv.reader(f)
        for row in reader:
            keys.append(row[1].strip())
    result = table.convert_article(keys)
    result = ''.join(res.word for res in result)
    result = '运行状态sign搜索码表sign按键统计signsign分析sign加载个人及系统配置文件用了numbernumbernumber毫秒sign故意输错sign其实根本没有错的啦'
