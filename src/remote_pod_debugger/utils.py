"""

utils module
"""
from enum import Enum


class Colors(Enum):
    """

    ANSI Codes
    """

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def info(msg: str):
    """

    print info message
    """
    print(Colors.OKGREEN.value + msg + Colors.ENDC.value)


def debug(msg: str):
    """

    print debug message
    """
    print(Colors.OKCYAN.value + msg + Colors.ENDC.value)


def warning(msg: str):
    """

    print warning message
    """
    print(Colors.WARNING.value + msg + Colors.ENDC.value)
