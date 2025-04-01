import os
import uuid
import re

from datetime import datetime, timezone

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.db import db
from src.models.blacklist import Blacklist

blacklist_blueprint = Blueprint("blacklist", __name__)

EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

def is_valid_uuid(value: str) -> bool:
    try:
        uuid_obj = uuid.UUID(value)
        return str(uuid_obj) == value
    except ValueError:
        return False

def validate_all_information(data: dict):
    fields = {"email","app_uuid", "blocked_reason"}
    return fields.issubset(data.keys())

@blacklist_blueprint.route("/blacklists/<email>", methods=["GET"])
@jwt_required()
def get_route(email):
    if not re.match(EMAIL_REGEX, email):
        return jsonify({'message': 'Formato de correo electrónico inválido'}), 400

    blacklists = Blacklist.query.filter_by(email=email).all()

    if not blacklists:
        return jsonify({
            'message': 'El usuario no está bloqueado',
            'isBlocked': False,
            'reasons': []
        }), 200

    reasons = [{
            "reason": blacklist.reason,

        } for blacklist in blacklists]
    return jsonify({
        'message': 'El usuario está bloqueado',
        'isBlocked': True,
        'reasons': reasons
    }), 200


@blacklist_blueprint.route("/blacklists/token", methods=["GET"])
def get_token():
    access_token = create_access_token(identity="1")

    return jsonify({'token': access_token}), 200

@blacklist_blueprint.route("/blacklists", methods=["POST"])
@jwt_required()
def add_to_blacklist():
    data = request.get_json()

    if not data or "email" not in data or "app_uuid" not in data:
        return jsonify({'message': 'Faltan campos obligatorios'}), 400

    email = data.get("email")
    app_uuid = data.get("app_uuid")
    reason = data.get("blocked_reason", "")

    if not re.match(EMAIL_REGEX, email):
        return jsonify({'message': 'Formato de correo electrónico inválido'}), 400

    if not is_valid_uuid(app_uuid):
        return jsonify({'message': 'UUID de la app inválido'}), 400

    if len(reason) > 255:
        return jsonify({'message': 'El motivo no puede exceder 255 caracteres'}), 400

    ip_address = request.remote_addr or request.headers.get('X-Forwarded-For', 'Unknown')

    new_entry = Blacklist(
        email=email,
        app_id=app_uuid,
        reason=reason,
        ip_address=ip_address,
        timestamp=datetime.now(timezone.utc)
    )

    try:
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({'message': 'Email agregado a la lista negra exitosamente'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error al guardar en la base de datos', 'error': str(e)}), 500
