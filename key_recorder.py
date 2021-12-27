from infi.systray import SysTrayIcon


if __name__ == "__main__":
    import utils

    import os
    import signal

    pid = os.getpid()

    menu_options = (
        # ("Refresh state", None, lambda self: utils.get_state(self, port)),
        # ("Start", None, lambda self: utils.set_state(self, port, True)),
        # ("Stop", None, lambda self: utils.set_state(self, port, False))
    )
    systray = SysTrayIcon("icon.ico", "Running: False",
                          menu_options, lambda self: os.kill(pid, signal.SIGTERM))
    systray.start()
