from flask import Flask
from config import config
from .meta import bootstrap, mail, moment, db

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config['development'])
    config['development'].init_app(app)

    print(dir(config['development']))
    print(app.config['SQLALCHEMY_DATABASE_URI'])

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
