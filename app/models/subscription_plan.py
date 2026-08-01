from app.extensions import db

class SubscriptionPlan(db.Model):
    __tablename__ = "subscription_plans"
    
    subscription_plan_id = db.Column(
        db.Integer,
        primary_key = True
    )
    
    plan_name = db.Column(
        db.String(100),
        nullable = False
    )
    
    plan_type = db.Column(
        db.Enum(
            "Free",
            "Standard",
            "Premium",
            name = "plan_type_enum"
        ),
        nullable = False
    )
    
    monthly_price = db.Column(
        db.Numeric(10, 2),
        nullable = False
    )
    
    description = db.Column(
        db.Text,
        nullable = True
    )
    
    benifits = db.Column(
        db.Text,
        nullable = True
    )
    
    is_active = db.Column(
        db.Boolean,
        nullable = False,
        default=True
    )
    
    users = db.relationship(
        "User",
        backref = "subscription_plan",
        lazy = True
    )