import os
import uuid

from flask import Flask
from flask_jwt_extended import JWTManager

from src.db import db, reset_database
from src.config import Config
from src.blueprints.blacklist import blacklist_blueprint
from src.models.blacklist import Blacklist
from datetime import datetime, timezone

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI", "sqlite:///blacklists.db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    JWTManager(app)
    db.init_app(app)

    with app.app_context():
        reset_database()
        print("Tablas creadas y listas para usar")
        ## CREO REGISTROS DE PRUEBA
        blacklist1 = Blacklist(
            id=str(uuid.uuid4()),
            app_id=str(uuid.uuid4()),
            email='test1@test.co',
            reason='Es molesto',
            ip_address="127.0.0.1",
            timestamp=datetime.now(timezone.utc)
        )
        blacklist2 = Blacklist(
            id=str(uuid.uuid4()),
            app_id=str(uuid.uuid4()),
            email='test1@test.co',
            reason='Es molesto',
            ip_address="127.0.0.1",
            timestamp=datetime.now(timezone.utc)
        )
        blacklist3 = Blacklist(
            id=str(uuid.uuid4()),
            app_id=str(uuid.uuid4()),
            email='test2@test.co',
            reason='Es molesto',
            ip_address="127.0.0.1",
            timestamp=datetime.now(timezone.utc)
        )

        db.session.add(blacklist1)
        db.session.add(blacklist2)
        db.session.add(blacklist3)
        db.session.commit()

    app.register_blueprint(blacklist_blueprint)

    return app