from infi.systray import SysTrayIcon
import socket
import requests


def is_open(port, s=None):
    if s is None:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(('localhost', port))
        s.shutdown(2)
        return False
    except:
        return True


def get_open_port(default_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if is_open(default_port, s):
        s.close()
        return default_port

    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port


def set_state(self: SysTrayIcon, port: int, running: bool):
    rep = requests.post(
        f"http://localhost:{port}/api/set_hook_state", params={'running': running})
    get_state(self, port)


def get_state(self: SysTrayIcon, port: int):
    rep = requests.get(f"http://localhost:{port}/api/get_hook_state")
    self.update(hover_text=f"running:{rep.json()['running']}")
