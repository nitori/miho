

from flask import Blueprint, url_for

from .. import utils

web = Blueprint('web', __name__)


@web.route('/')
def index():

    images = list(utils.get_images())
    images.sort()

    s = ''
    for im in images:
        turl = url_for('static', filename=f'thumbs/{im.thumbnail}')
        iurl = url_for('static', filename=im.fullname)
        s += f'<a href="{iurl}"><img src="{turl}"></a> '

    return s
