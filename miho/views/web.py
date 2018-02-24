
from flask import Blueprint, render_template

from .. import utils

web = Blueprint('web', __name__)


@web.route('/')
def index():
    images = list(utils.get_images())
    images.sort()
    return render_template('index.html', images=images)
