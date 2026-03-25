from flask import Flask

from .config import Config
from .routes import api_blueprint


def create_app(config_class: type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.register_blueprint(api_blueprint)

    return app
