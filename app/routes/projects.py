from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import Project
from app.extensions import db

projects_bp = Blueprint("projects", __name__)

def project_to_dict(p: Project):
    return {
        "id": p.id,
        "title": p.title,
        "description": p.description,
        "tech_stack": p.tech_stack,
        "link": p.link,
        "order_index": p.order_index,
        "created_at": p.created_at.isoformat()
    }

@projects_bp.get("/")
def get_projects():
    projects = (
        Project.query
        .order_by(Project.order_index.asc(), Project.created_at.desc())
        .all()
    )
    return jsonify([project_to_dict(p) for p in projects])

@projects_bp.get("/<int:project_id>")
def get_project(project_id: int):
    project = Project.query.get_or_404(project_id)
    return jsonify(project_to_dict(project))

@projects_bp.post("/")
@jwt_required()
def create_project():
    data = request.get_json(silent=True) or {}

    title = data.get("title")
    description = data.get("description")
    if not title or not description:
        return jsonify({"error": "title and description are required"}), 400

    # If order_index not provided, auto-place at the bottom (largest + 1)
    provided_order = data.get("order_index")
    if provided_order is None:
        max_order = db.session.query(db.func.max(Project.order_index)).scalar()
        next_order = (max_order + 1) if max_order is not None else 0
        order_index = next_order
    else:
        try:
            order_index = int(provided_order)
        except (TypeError, ValueError):
            return jsonify({"error": "order_index must be an integer"}), 400

    project = Project(
        title=title,
        description=description,
        tech_stack=data.get("tech_stack"),
        link=data.get("link"),
        order_index=order_index
    )
    db.session.add(project)
    db.session.commit()
    return jsonify(project_to_dict(project)), 201

@projects_bp.put("/<int:project_id>")
@jwt_required()
def update_project(project_id: int):
    project = Project.query.get_or_404(project_id)
    data = request.get_json(silent=True) or {}

    # Patch update: only update provided fields
    if "title" in data:
        if not data["title"]:
            return jsonify({"error": "title cannot be empty"}), 400
        project.title = data["title"]

    if "description" in data:
        if not data["description"]:
            return jsonify({"error": "description cannot be empty"}), 400
        project.description = data["description"]

    if "tech_stack" in data:
        project.tech_stack = data["tech_stack"]

    if "link" in data:
        project.link = data["link"]

    if "order_index" in data:
        try:
            project.order_index = int(data["order_index"])
        except (TypeError, ValueError):
            return jsonify({"error": "order_index must be an integer"}), 400

    db.session.commit()
    return jsonify(project_to_dict(project))

@projects_bp.delete("/<int:project_id>")
@jwt_required()
def delete_project(project_id: int):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return jsonify({"message": "Project deleted"})
