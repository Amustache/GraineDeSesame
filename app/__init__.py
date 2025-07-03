from flask import Flask


from app.config import Config
from app.extensions import db
from app.main.utilities import hash_password, check_hash, random_books


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)

    app.jinja_env.globals.update(hash_password=hash_password)
    app.jinja_env.globals.update(check_hash=check_hash)
    app.jinja_env.globals.update(random_books=random_books)

    # Register blueprints here
    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    return app
