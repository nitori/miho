
from functools import partial

from flask import Flask
from werkzeug.routing import BaseConverter

from . import utils


def create_app(config_file) -> Flask:
    app = Flask(__name__, static_url_path='/images', static_folder='../images')
    app.config.from_pyfile(str(config_file))
    app.url_map.converters['color'] = ColorConverter
    register_blueprints(app)
    return app


def register_blueprints(app: Flask):
    from .views.api import api
    from .views.web import web

    api.before_request(partial(utils.restrict_with_base_auth, 'API'))
    web.before_request(partial(utils.restrict_with_base_auth, 'WEB'))

    app.register_blueprint(web)
    app.register_blueprint(api, url_prefix='/api')


class ColorConverter(BaseConverter):
    regex = r'([a-fA-F0-9]{3}|[a-fA-F0-9]{6})'
