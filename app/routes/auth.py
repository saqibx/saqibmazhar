from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    if (username == current_app.config["ADMIN_USERNAME"]
        and password == current_app.config["ADMIN_PASSWORD"]):
        token = create_access_token(identity="admin")
        return jsonify(access_token=token)

    return jsonify({"error": "Invalid credentials"}), 401
