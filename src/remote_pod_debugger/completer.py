"""

Completer
"""
import atexit
import readline
import os


HISTFILE = os.path.join(os.path.expanduser("~"), ".config", ".remote_debugger")
MAX_HISTORY_LENGTH = 1000


class Completer:  # pylint: disable=too-few-public-methods
    """

    Completer class
    """

    def __init__(self, options: list):
        self._options = sorted(options)
        self._matches = None

    def complete(self, text: str, state: int):
        """

        complete function, return response if an option match input
        """
        response = None
        if state == 0:
            if text:
                self._matches = [s for s in self._options if s and s.startswith(text)]
            else:
                self._matches = self._options[:]
        try:
            response = self._matches[state]
        except IndexError:
            response = None
        return response


def save_history(prev_h_len: int):
    """

    save readline history
    """
    new_h_len = readline.get_current_history_length()
    readline.set_history_length(MAX_HISTORY_LENGTH)
    readline.append_history_file(new_h_len - prev_h_len, HISTFILE)


def activate_history():
    """

    activate history
    """
    try:
        readline.read_history_file(HISTFILE)
        h_len = readline.get_current_history_length()
    except FileNotFoundError:
        open(HISTFILE, "wb").close()
        h_len = 0

    atexit.register(save_history, h_len)
    readline.parse_and_bind("tab: complete")
    readline.parse_and_bind("set editing-mode vi")
