
import pathlib
import random
import string

from flask import current_app


def randstr(length):
    s = string.ascii_letters + string.digits
    return ''.join(random.choice(s) for _ in range(length))


def get_root() -> pathlib.Path:
    return pathlib.Path(current_app.root_path).absolute().parent
