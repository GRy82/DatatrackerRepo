import os

from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import videogame
    app.register_blueprint(videogame.bp)

    app.add_url_rule('/', endpoint='videogame.index')

    return app
