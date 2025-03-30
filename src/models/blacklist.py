import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer
from src.db import db
from werkzeug.security import generate_password_hash, check_password_hash

class Blacklist(db.Model):
    __tablename__ = "blacklists"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    app_id = Column(String(50),  nullable=False)
    email = Column(String(100), nullable=False)
    reason = Column(String(100), nullable=False)
    ip_address = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)