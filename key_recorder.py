from collections import deque
import threading

import word_handler
import keyboard
import ctypes
ctypes.windll.user32.SetProcessDPIAware()

import PySimpleGUI as sg

layout = [[sg.Text("", auto_size_text=True, key="-pbyb-"), sg.Checkbox("跟随", enable_events=True, key="Follow"), sg.Button("开始", key="Toggle")],
          [sg.Text("", auto_size_text=True, key="-hjzi-"), sg.Button("关闭", key="Cancel")]]
win = sg.Window("key optimizer", layout, no_titlebar=True,
                keep_on_top=True, alpha_channel=.7, grab_anywhere=True, font="微软雅黑")

remover = None
word_getter = None
code = deque()
now_word = deque()
win_pos = word_handler.win_position.WinPosition()


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
                case _:
                    yield key

    try:
        for word in table.convert_article(get_key()):
            win.write_event_value("-WORD-", word)
    except Exception as e:
        import logging
        logging.getLogger("exception").exception(e)


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
            case "Toggle":
                button: sg.Button = win["Toggle"]
                if remover is not None:
                    button.update("开始")
                    remover()
                    remover = None
                    word_handler.record.queue.put("Stop")
                else:
                    button.update("停止")
                    threading.Thread(target=get_word, args=(
                        win,), daemon=True).start()
                    remover = keyboard.hook(word_handler.record.record)

            case "Follow":
                # cannot update in here, because there is not caret when toggling checkbox
                if not values["Follow"]:
                    win_pos.clear()

            case "-MOVE-":
                win.move(*word_handler.get_win.get_cursor_position())
                win_pos.clear()

            case "-WORD-":
                word: word_handler.code_table.InputWord = values["-WORD-"]
                if word is None:
                    continue
                now_word.append(word.word)
                code.append(word.code)
                while not table.match_exact_word("".join(now_word), 1, False):
                    now_word.popleft()
                    code.popleft()
                ret = table.match_exact_word("".join(now_word), 100, True)
                if ret:
                    ret.sort(key=lambda word: len(word.code))
                    ret = ret[0]
                    if len(ret.code) < len(" ".join(code)):
                        pbyb: sg.Text = win["-pbyb-"]
                        pbyb.update(ret.code)
                        hjzi: sg.Text = win["-hjzi-"]
                        hjzi.update(ret.word)

                if values["Follow"]:
                    pos = win_pos.get_pos(win.current_location())
                    if not pos:
                        continue
                    win.move(*pos)
    except Exception as e:
        import logging
        logging.getLogger("exception").exception(e)

win.close()
