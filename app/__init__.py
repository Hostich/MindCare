from flask import Flask
from app.models import User

from config import Config
from app.extensions import db, migrate, login_manager, mail, socketio
from app.routes.landingpage import lpage
from app.routes.authorization import auth
from app.routes.profile import profile
from app.routes.community import community
from app.routes.chat_request import chat_request
from app.routes.volunteer import volunteer
from app.routes.mood import mood
from app.routes.seeker import seeker
from app.socket import chat_events

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    socketio.init_app(app)
    
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to continue."
    login_manager.login_message_category = "warning"
    
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))
    
    app.register_blueprint(lpage)
    app.register_blueprint(auth)
    app.register_blueprint(profile)
    app.register_blueprint(community)
    app.register_blueprint(chat_request)
    app.register_blueprint(volunteer)
    app.register_blueprint(mood)
    app.register_blueprint(seeker)

    return app