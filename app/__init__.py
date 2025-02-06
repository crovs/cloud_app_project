from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import quote as url_quote



db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/postgres'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    from .routes import main
    app.register_blueprint(main)
    
    return app
