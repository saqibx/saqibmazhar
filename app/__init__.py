from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from .config import Config
from .extensions import db, jwt

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)
    app.url_map.strict_slashes = False

    CORS(app)
    db.init_app(app)
    jwt.init_app(app)

    from .routes.projects import projects_bp
    from .routes.auth import auth_bp
    from .routes.contact import contact_bp

    app.register_blueprint(projects_bp, url_prefix="/api/projects")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(contact_bp, url_prefix="/api/contact")

    return app

