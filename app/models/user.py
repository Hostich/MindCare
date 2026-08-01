from flask_login import UserMixin
from app.extensions import db

class User(UserMixin, db.Model):
    __tablename__ = "users"
    
    user_id = db.Column(
        db.Integer,
        primary_key = True
    )
    
    subscription_plan_id = db.Column(
        db.Integer,
        db.ForeignKey("subscription_plans.subscription_plan_id"),
        nullable=True
    )
    
    first_name = db.Column(
        db.String(50),
        nullable = True
    )
    
    last_name = db.Column(
        db.String(50),
        nullable = True
    )
    
    username = db.Column(
        db.String(50),
        unique = True,
        nullable = False
    )
    
    password = db.Column(
        db.String(255),
        nullable = False
    )
    
    email = db.Column(
        db.String(50),
        unique = True,
        nullable = False
    )
    
    phone_number = db.Column(
        db.String(15),
        nullable = True
    )
    
    occupation = db.Column(
        db.String(100),
        nullable = True
    )
    
    gender = db.Column(
        db.Enum(
            "Male",
            "Female",
            "Prefer not to say",
            name = "gender_enum" 
        ),
        nullable = True
    )
    
    profile_picture = db.Column(
        db.String(255),
        nullable = True
    )
    
    role = db.Column(
        db.Enum(
            "Admin",
            "Volunteer",
            "Counselor",
            "Seeker",
            name="role_enum"
        ),
        nullable = False,
        default = "Seeker"
    )
    
    account_status = db.Column(
        db.Enum(
            "Online",
            "Offline",
            name = "account_status_enum"
        ),
        nullable = False,
        default = "Offline"
    )
    
    created_at = db.Column(
        db.DateTime,
        server_default = db.func.now(),
        nullable = False
    )
    
    update_at = db.Column(
        db.DateTime,
        server_default = db.func.now(),
        onupdate = db.func.now(),
        nullable=True
    )
 
    def get_id(self):
        return str(self.user_id)
    
    post = db.relationship(
        "CommunityPost",
        backref="user",
        lazy=True
    )