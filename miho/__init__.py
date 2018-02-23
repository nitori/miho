
from flask import Flask


def create_app(config_file) -> Flask:
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    register_blueprints(app)
    return app


def register_blueprints(app: Flask):
    from .views.api import api
    from .views.web import web
    app.register_blueprint(web)
    app.register_blueprint(api, url_prefix='/api')
