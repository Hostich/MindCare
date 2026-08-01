from flask import Flask
from app.models import User, SubscriptionPlan, CommunityPost, MoodAssessment

from config import Config
from app.extensions import db, migrate, login_manager, mail
from app.routes.landingpage import lpage
from app.routes.authorization import auth
from app.routes.profile import profile
from app.routes.community import community
from app.routes.chat_request import chat_request
from app.routes.volunteer import volunteer

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    
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
    
    return app