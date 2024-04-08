from flask import Flask
import secrets
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_session import Session

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = secrets.token_hex(16)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = '/tmp/flask_session'
    app.config['PERMANENT_SESSION_LIFETIME'] = 4000
    app.config['SESSION_PERMANENT'] = True 

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    Session(app)
    
    from .models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth route
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # blueprint for reports routes 
    from .reports import reports as reports_blueprint
    app.register_blueprint(reports_blueprint)

    # blueprint for client routes 
    from .client import client as client_blueprint
    app.register_blueprint(client_blueprint)
    
    # blueprint for agent routes 
    from .agent import agent as agent_blueprint
    app.register_blueprint(agent_blueprint)
    
    return app