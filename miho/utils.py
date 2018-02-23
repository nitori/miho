
import typing as t
import pathlib
import random
import string
import os
import re
from collections import namedtuple

from flask import current_app

FN_PATTERN = re.compile(
    r'^(?P<index>\d{6})-(?P<filename>(?P<subhash>[a-f0-9]{17})-(?P<width>\d+)-(?P<height>\d+)\.(?P<ext>jpg|png|gif))$'
)

Image = namedtuple('Image', [
    'index', 'filename', 'subhash', 'width', 'height', 'ext', 'fullname',
    'preview', 'thumbnail'
])


def randstr(length):
    s = string.ascii_letters + string.digits
    return ''.join(random.choice(s) for _ in range(length))


def get_root() -> pathlib.Path:
    return pathlib.Path(current_app.root_path).absolute().parent


def match_image(filename):
    return FN_PATTERN.match(filename)


def get_images_dir() -> pathlib.Path:
    return pathlib.Path(
        get_root(),
        current_app.config.get('IMAGES_DIR', 'images')
    )


def get_images() -> t.Generator[Image, None, None]:
    images_dir = get_images_dir()
    for fn in os.listdir(images_dir):
        m = match_image(fn)
        if m is not None:
            yield Image(
                int(m.group('index')),
                m.group('filename'),
                m.group('subhash'),
                int(m.group('width')),
                int(m.group('height')),
                m.group('ext'),
                m.group(0),
                f"{m.group('index')}-1-{m.group('filename')}.jpg",
                f"{m.group('index')}-2-{m.group('filename')}.jpg",
            )
