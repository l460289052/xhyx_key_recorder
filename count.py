from itertools import chain
from typing import Iterable
from dataclasses import dataclass
from pathlib import Path


@dataclass
class FileInfo:
    path: Path
    length: int


def count(path: Path, recurrent: bool, exts: set):
    for p in path.iterdir():
        if recurrent and p.is_dir():
            yield from count(p, recurrent, exts)
        elif p.suffix.lower() in exts:
            with p.open('r', encoding='utf-8') as f:
                cnt = len([line for line in f if line.strip()])
                yield FileInfo(p, cnt)


if __name__ == "__main__":
    root = Path(__file__).parent.absolute()
    cnt = 0
    for info in chain(
            count(Path('server').absolute(), True, {'.py'}),
            count(Path('client/src').absolute(), True, {'.css', '.jsx', '.js'})):
        print(f'{info.length} {info.path.relative_to(root)}')
        cnt += info.length
    print(f"total:{cnt}")
