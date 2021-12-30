import ctypes
import os
import pathlib
import threading
from collections import deque
from PySimpleGUI.PySimpleGUI import popup_notify

import keyboard

import word_handler
from word_handler import code_table

ctypes.windll.user32.SetProcessDPIAware()

import PySimpleGUI as sg

layout = [
    [
        sg.Text("", auto_size_text=True, key="-pbyb-"),
        sg.ButtonMenu("更多", ["", ["转换", "打开LOG"]], key="-MORE-")],
    [
        sg.Text("", auto_size_text=True, key="-hjzi-"),
        sg.Button("关闭", key="Cancel")]]
win = sg.Window("key optimizer", layout, no_titlebar=True,
                keep_on_top=True, alpha_channel=.7, grab_anywhere=True, font="微软雅黑")

remover = None
word_getter = None
code = deque()
now_word = deque()


table = word_handler.code_table.get_table()


def get_word(win: sg.Window):
    def get_key():
        while True:
            key = word_handler.record.queue.get()
            match key:
                case "Stop":
                    return
                case "-MOVE-":
                    win.write_event_value("-MOVE-", True)
                case None:
                    pass
                case _:
                    yield key

    try:
        for word in table.convert_article(get_key()):
            win.write_event_value("-WORD-", word)
    except Exception as e:
        import logging
        logging.getLogger("exception").exception(e)


threading.Thread(target=get_word, args=(
    win,), daemon=True).start()
remover = keyboard.hook(word_handler.record.record)

while True:
    event, values = win.read()
    try:
        # print(event, values)
        match event:
            case sg.WIN_CLOSED | "Cancel":
                if remover is not None:
                    remover()
                    word_handler.record.queue.put("Stop")
                break

            case "-MOVE-":
                win.move(*word_handler.get_win.get_cursor_position())

            case "-WORD-":
                word: word_handler.code_table.InputWord = values["-WORD-"]
                if word is None:
                    continue
                now_word.append(word.word)
                if word.committer:
                    code.append(word.code + " ")
                else:
                    code.append(word.code)
                while not table.match_exact_word("".join(now_word), 1, False):
                    now_word.popleft()
                    code.popleft()
                ret = table.match_exact_word("".join(now_word), 100, True)
                if ret:
                    ret.sort(key=lambda word: len(word.code))
                    ret = ret[0]
                    if len(ret.code) + 1 < len("".join(code)):
                        pbyb: sg.Text = win["-pbyb-"]
                        pbyb.update(ret.code)
                        hjzi: sg.Text = win["-hjzi-"]
                        hjzi.update(ret.word)

            case "-MORE-":
                match values["-MORE-"]:
                    case "转换":
                        try:
                            f_in = sg.filedialog.askopenfilename(
                                title="请选择安卓百度个性短语文件", filetypes=(("安卓个性短语文件", '*.ini'),))
                            if f_in:
                                f_in = pathlib.Path(f_in)
                                f_out = sg.filedialog.asksaveasfilename(
                                    defaultextension=".txt",
                                    filetypes=(("词库文件", '*.txt'),))
                                if f_out:
                                    f_out = pathlib.Path(f_out)
                                    word_handler.code_table.convert_from_andriod(
                                        f_in, f_out)
                                else:
                                    raise ValueError()
                            else:
                                raise ValueError()
                        except ValueError:
                            sg.popup_notify(title="已取消")

                    case "打开LOG":
                        os.system(
                            f"notepad {word_handler.config.LOG_DIR.joinpath('exception.txt').absolute()}")

    except Exception as e:
        import logging
        logging.getLogger("exception").exception(e)

win.close()
