from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from flask_redis import FlaskRedis

db = SQLAlchemy()
migrate = Migrate()
redis_store = FlaskRedis()


def create_app(config_class=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    app.config['ASSETS_DEBUG'] = True
    app.static_url_path = app.config.get('STATIC_FOLDER')
    app.static_folder = app.root_path + app.static_url_path
    redis_store.init_app(app, charset='utf-8', decode_responses=True)

    """these are blueprints - a way of making a Flask application more modular and re-usable"""
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.submit import bp as submit_bp
    app.register_blueprint(submit_bp, url_prefix='/submit')

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app


from app import models
