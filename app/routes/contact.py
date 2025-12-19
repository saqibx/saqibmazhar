from flask import Blueprint, request, jsonify
from app.models import ContactMessage
from app.extensions import db

contact_bp = Blueprint("contact", __name__)

@contact_bp.post("/")
def submit_message():
    data = request.json
    msg = ContactMessage(
        name=data.get("name"),
        email=data.get("email"),
        message=data["message"]
    )
    db.session.add(msg)
    db.session.commit()
    return jsonify({"message": "Message received"}), 201
