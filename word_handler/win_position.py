from . import get_win


class WinPosition:
    def __init__(self) -> None:
        self.x_bias = None
        self.y_bias = None
        self.pos = None

    def update(self, win_pos):
        pos = get_win.get_caret_position()
        if pos:
            self.x_bias = win_pos[0] - pos[0]
            self.y_bias = win_pos[1] - pos[1]
            self.pos = win_pos

    def get_pos(self, win_pos):
        if self.pos is None:
            self.update(win_pos)
            return None
        if self.x_bias is None:
            return None
        pos = get_win.get_caret_position()
        print(pos)
        if pos:
            self.pos = (pos[0] + self.x_bias, pos[1] + self.y_bias)
            return self.pos
        else:
            return None

    def clear(self):
        self.x_bias = self.y_bias = self.pos = None
