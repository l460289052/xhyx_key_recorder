from itertools import chain
import logging
import math
import pathlib
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Iterable, List, Tuple, Deque
from collections import deque

from sortedcontainers import SortedKeyList

from .config import WORD_DIR

number_key = set(map(str, range(10)))
sign_key = set(',.":[]{}\\\|~!@#$%^&*()-=_+`')
select_key = {'space': 0, ';': 1, "'": 2}
alphabet_key = {chr(ord('a') + i) for i in range(26)}
alphabet_key.update({chr(ord('A') + i) for i in range(26)})
for i in number_key:
    select_key[i] = int(i)

shown_word = {
    'space': ' ',
    'backspace': '<-'
}


class CodeType(str, Enum):
    Word = "Word"
    Undefine = "Undefine"
    Sign = "Sign"
    Num = "Num"
    Alpha = "Alpha"


@dataclass
class TableWord:
    code: str
    word: str
    file: str
    top: bool = False
    priority: int = None

    @property
    def key(self):
        return self.code, not self.top, -(self.priority or 0)

    def __str__(self) -> str:
        return f"{self.code} {self.word} in {self.file}"

    def dict(self):
        return {
            "code": self.code,
            "word": self.word,
            "file": self.file
        }


@dataclass
class InputWord:
    code: str
    word: str
    committer: str
    typ: CodeType = CodeType.Word

    @classmethod
    def special(cls, code, committer, typ: CodeType):
        return cls(code, shown_word.get(code, code), committer, typ)

    def dict(self):
        return {
            "code": self.code,
            "word": self.word,
            "committer": self.committer,
            "type": self.typ.value
        }


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

                word = TableWord(row[1], row[0], file_name,
                                 top, float(row[2]) if len(row) > 2 else None)
                ret.append(word)
            except:
                exception = logging.getLogger('exception')
                exception.info(f"无法识别此行：{line}，位于文件{file_name}的{line_number}行")

        return ret


class CodeTable:
    def __init__(self) -> None:
        self.words: List[TableWord] = []
        self.codes_dict: SortedKeyList[TableWord] = SortedKeyList(
            key=lambda word: word.key)
        self.words_dict: SortedKeyList[TableWord] = SortedKeyList(
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

    def load(self):
        self.clear()

        for p in WORD_DIR.iterdir():
            if p.suffix.lower() == '.txt':
                self.words.extend(read_from_file(p))
        self.codes_dict.update(self.words)
        self.words_dict.update(self.words)
        self.modify_time = datetime.now()

    def match_exact_code(self, pattern, max_number, same: bool) -> List[TableWord]:
        position = self.codes_dict.bisect_key_left((pattern, False, -math.inf))
        ret = []
        while position < len(self.codes_dict):
            word: TableWord = self.codes_dict[position]
            if (word.code == pattern if same else word.code.startswith(pattern)):
                ret.append(word)
                if len(ret) > max_number:
                    break
            else:
                break
            position += 1
        return ret

    def match_exact_word(self, pattern, max_number, same: bool) -> List[TableWord]:
        position = self.words_dict.bisect_key_left(pattern)
        ret = []
        while position < len(self.words_dict):
            word: TableWord = self.words_dict[position]
            if (word.word == pattern if same else word.word.startswith(pattern)):
                ret.append(word)
                if len(ret) > max_number:
                    break
            else:
                break
            position += 1
        return ret

    def convert_article(self, keys: Iterable[str]) -> Iterable[InputWord]:
        stack = []
        for key in keys:
            key = key.strip()
            if key == 'backspace':
                if stack:
                    stack.pop()
                else:
                    yield InputWord.special(key, '', CodeType.Sign)
            if key == 'enter' or key == 'esc' or key == 'shift':
                if key != 'esc':
                    if stack:
                        yield InputWord.special(''.join(stack), key, CodeType.Alpha)
                    elif key != 'shift':
                        yield InputWord.special(key, '', CodeType.Sign)
                stack.clear()
            elif key in select_key:
                if stack:
                    yield self.select_th(''.join(stack), key)
                    stack.clear()
                else:
                    yield InputWord.special(key, '', CodeType.Num if key in number_key else CodeType.Sign)
            elif key in sign_key:
                if stack:
                    yield self.select_th(''.join(stack), key)
                    stack.clear()
                yield InputWord.special(key, '', CodeType.Sign)
            elif key not in alphabet_key:
                continue
            elif len(stack) < 4:
                stack.append(key)
                if len(stack) == 4:
                    code = ''.join(stack)
                    words = self.match_exact_code(code, 2, False)
                    if len(words) == 1:
                        yield InputWord(code, words[0].word, '')
                        stack.clear()
            else:
                code = ''.join(stack)
                words = self.match_exact_code(code, 1, False)
                if words:
                    yield InputWord(code, words[0].word, '')
                    stack.clear()
                stack.append(key)

    def optim_article(self, article: Iterable[InputWord]) -> Iterable[Tuple[List[InputWord], List[InputWord]]]:
        old_words: Deque[InputWord] = deque()
        last_str: str = ''
        last_codes: List[TableWord] = None

        for word in chain(article, [InputWord('stopper', '!@#$', '')]):
            tmp_str = last_str + word.word

            tmp_codes = self.match_exact_word(
                tmp_str, 1000, False)
            if tmp_codes:
                old_words.append(word)
                last_codes = tmp_codes
                last_str = tmp_str
                continue
            elif not old_words:
                continue

            old_code = []
            for old_word in old_words:
                old_code.append(old_word.code + '*')

            old_code = ''.join(old_code)
            min_len = len(old_code) - 1
            if min_len == 4:
                min_len = 3
            ret = []
            for code in last_codes:
                words = self.match_exact_code(code.code, 100, True)
                for ind, new_word in enumerate(words):
                    if ind > 5:
                        break
                    if new_word.word == last_str:
                        code_len = len(new_word.code) + 1
                        if min_len >= code_len:
                            ret.append(
                                (code_len, list(old_words), [InputWord(new_word.code, new_word.word, str(ind + 1))]))
                            min_len = code_len
            for r in ret:
                if r[0] == min_len:
                    yield r[1], r[2]

            old_words.clear()
            tmp_str = word.word
            tmp_codes = self.match_exact_word(tmp_str, 1000, False)
            if tmp_codes:
                old_words.append(word)
                last_codes = tmp_codes
                last_str = tmp_str
            else:
                last_codes = None
                last_str = ''

    def select_th(self, code, slt_key):
        slt_num = select_key.get(slt_key, 0)
        words = self.match_exact_code(code, slt_num, False)
        if len(words) < slt_num + 1:
            return InputWord.special(code, slt_key, CodeType.Undefine)
        else:
            return InputWord(code, words[slt_num].word, slt_key)


_table: CodeTable = None


def get_table():
    global _table
    if _table is None:
        _table = CodeTable()
    if _table.need_load():
        _table.load()
    return _table
