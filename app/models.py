from .extensions import db
from datetime import datetime

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    tech_stack = db.Column(db.String(200))
    link = db.Column(db.String(200))

    # Timeline control: smaller = higher/earlier on your timeline
    order_index = db.Column(db.Integer, nullable=False, default=0, index=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
