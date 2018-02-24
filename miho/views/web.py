
from flask import Blueprint, render_template, Response

from .. import utils

web = Blueprint('web', __name__)


@web.route('/')
def index():
    images = list(utils.get_images())
    images.sort(reverse=True)
    return render_template('index.html', images=images)


@web.route('/spinner.svg')
def spinner():
    return Response(render_template('spinner.svg'), mimetype='image/svg+xml')
