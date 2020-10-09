from flask_bcrypt import generate_password_hash
from flask_restful import Resource, reqparse

from models.user import UserModel
from werkzeug.security import safe_str_cmp
import uuid

from app import app


class Setup(Resource):

    def get(self, password):
        if not password:
            return {"msg": "access denied"}, 404
        if not safe_str_cmp(password, app.config['SETUP_KEY']):
            return {"msg": "access denied"}, 403
        log = "Creating user... "
        default_admin = UserModel.find_by_username(app.config['DEFAULT_ADMIN_NAME'])
        if default_admin:
            log += "Default admin already exist"
            default_admin.password = generate_password_hash(app.config['DEFAULT_ADMIN_PASSWORD']).decode('utf-8')
            default_admin.save_to_db()
        else:
            unique_id = str(uuid.uuid4())
            new_admin = UserModel(unique_id,
                                  (generate_password_hash(app.config['DEFAULT_ADMIN_PASSWORD'])).decode('utf-8'), True,
                                  app.config['DEFAULT_ADMIN_NAME'], app.config['DEFAULT_ADMIN_EMAIL'], "")
            log += "Default user created"
            new_admin.save_to_db()

        return {"msg": log}, 201
