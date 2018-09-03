import os

from flask import Flask
from . import db
from . import auth
from . import welcome
from . import client
from . import product


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'helloflask.sqlite'),
    )
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(welcome.bp)
    app.register_blueprint(client.bp)
    app.register_blueprint(product.bp)
    app.add_url_rule('/', endpoint='welcome')
    app.add_url_rule('/client', endpoint='index')

    return app
