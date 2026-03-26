from flask import Flask

from app.api import api_bp
from app.config import Config
from app.state.cart_store import InMemoryCartStore


def create_app(config_object: type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.extensions["cart_store"] = InMemoryCartStore()
    app.register_blueprint(api_bp)
    return app
