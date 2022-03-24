import logging
import os

from flask import Flask, current_app, request
from flask_argon2 import Argon2
from flask_babel import Babel
from flask_babel import lazy_gettext as _l
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_moment import Moment
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy

try:
    from fakeredis import FakeRedis as Redis
except ImportError:
    from redis import Redis

argon2 = Argon2()
db = SQLAlchemy()
mi = Migrate()
bootstrap = Bootstrap5()
lm = LoginManager()
lm.session_protection = "strong"
lm.login_view = "login"
lm.login_message = _l('Please log in to access this page.')
lm.login_message_category = "info"
moment = Moment()
babel = Babel()
# cache = FlaskRedis()
cache = FlaskRedis.from_custom_provider(Redis)


def create_app(config, **kwargs):

    logging.basicConfig(level=logging.INFO)

    app = Flask(__name__, **kwargs)
    app.config.from_object(config)

    argon2.init_app(app)

    db.init_app(app)
    # mi.init_app(app, db, render_as_batch=True)
    mi.init_app(app, db)
    bootstrap.init_app(app)
    lm.init_app(app)
    moment.init_app(app)
    babel.init_app(app)
    cache.init_app(app)

    from app.auth import bp as auth_bp
    from app.errors import bp as errors_bp
    from app.main import bp as main_bp

    app.register_blueprint(errors_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])


from app import models  # noqa:F401,E402
