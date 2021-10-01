import math
import logging
from datetime import datetime
import pathlib
from dataclasses import dataclass
from typing import List

from sortedcontainers import SortedKeyList

from ..config import WORD_DIR


@dataclass
class Word:
    file: str
    code: str
    word: str
    top: bool = False
    priority: int = None

    @property
    def key(self):
        return self.code, not self.top, -(self.priority or 0)

    def __str__(self) -> str:
        return f"{self.code} {self.word} in {self.file}"


def read_from_file(file_path: pathlib.Path):
    file_name = file_path.name
    with file_path.open('r', encoding='utf-8') as f:
        ret = []
        for line_number, line in enumerate(f):
            line = line.strip()
            try:
                if not line or line.startswith('#') or line.startswith('---'):
                    continue
                row = line.split('\t')
                if len(row) < 2:
                    raise ValueError()

                if '#' in row[1]:
                    top = True
                    row[1] = row[1].split('#')[0]
                else:
                    top = False

                word = Word(file_name, row[1], row[0],
                            top, float(row[2]) if len(row) > 2 else None)
                ret.append(word)
            except:
                exception = logging.getLogger('exception')
                exception.info(f"无法识别此行：{line}，位于文件{file_name}的{line_number}行")

        return ret


class CodeTable:
    def __init__(self) -> None:
        self.words: List[Word] = []
        self.codes_dict: SortedKeyList[Word] = SortedKeyList(
            key=lambda word: word.key)
        self.words_dict: SortedKeyList[Word] = SortedKeyList(
            key=lambda word: word.word)
        self.modify_time = datetime.now()

    def clear(self):
        self.words.clear()
        self.codes_dict.clear()
        self.words_dict.clear()

    def need_load(self):
        if len(self.words) == 0:
            return True
        for p in WORD_DIR.iterdir():
            if p.suffix.lower() == '.txt' and datetime.fromtimestamp(p.stat().st_mtime) > self.modify_time:
                return True
        return False

    def load_from(self):
        self.clear()

        for p in WORD_DIR.iterdir():
            if p.suffix.lower() == '.txt':
                self.words.extend(read_from_file(p))
        self.codes_dict.update(self.words)
        self.words_dict.update(self.words)
        self.modify_time = datetime.now()

    def match_exact_code(self, pattern, max_number, same: bool) -> List[Word]:
        position = self.codes_dict.bisect_key_left((pattern, False, -math.inf))
        ret = []
        while position < len(self.codes_dict):
            word: Word = self.codes_dict[position]
            if (word.code == pattern if same else word.code.startswith(pattern)):
                ret.append(word)
                if len(ret) > max_number:
                    break
            else:
                break
            position += 1
        return ret


_table: CodeTable = None


def get_table():
    global _table
    if _table is None:
        _table = CodeTable()
    if _table.need_load():
        _table.load_from()
    return _table
