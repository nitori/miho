
import typing as t
import pathlib
import random
import string
import os
import re
from collections import namedtuple

from flask import current_app, abort, request, Response

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
        current_app.config.get('MIHO_IMAGES_DIR', 'images')
    )


def match_to_tuple(match):
    return Image(
        int(match.group('index')),
        match.group('filename'),
        match.group('subhash'),
        int(match.group('width')),
        int(match.group('height')),
        match.group('ext'),
        match.group(0),
        f"{match.group('index')}-1-{match.group('filename')}.jpg",
        f"{match.group('index')}-2-{match.group('filename')}.jpg",
    )


def get_images() -> t.Generator[Image, None, None]:
    images_dir = get_images_dir()
    for fn in os.listdir(images_dir):
        m = match_image(fn)
        if m is not None:
            yield match_to_tuple(m)


def restrict_with_base_auth(conf_key_prefix):
    if request.authorization:
        username = request.authorization.get('username', None)
        password = request.authorization.get('password', None)
        admin_user = current_app.config.get(f'MIHO_{conf_key_prefix}_USER', randstr(20))
        admin_pass = current_app.config.get(f'MIHO_{conf_key_prefix}_PASS', randstr(20))
        if username == admin_user and password == admin_pass:
            return
        abort(401)
    auth_response = Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )
    abort(401, response=auth_response)
