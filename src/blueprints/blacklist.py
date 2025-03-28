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
            'isBlocked': False
        }), 200

    reasons = [{
            "reason": blacklist.reason,

        } for blacklist in blacklists]
    return jsonify({
        'isBlocked': True,
        'reasons': reasons
    }), 200





@blacklist_blueprint.route("/blacklists/token", methods=["GET"])
def get_token():
    access_token = create_access_token(identity="1")

    return jsonify({'token': access_token}), 200