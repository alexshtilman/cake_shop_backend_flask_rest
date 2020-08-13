from flask_bcrypt import generate_password_hash
from flask_restful import Resource,reqparse

from models.role import RoleModel
from models.user import UserModel
from werkzeug.security import safe_str_cmp

from app import app

class Setup(Resource):
    parser = reqparse.RequestParser()

    def get(self, password):
        if not password:
            return {"msg": "access denied"}, 404
        if not safe_str_cmp(password, app.config['SETUP_KEY']):
            return {"msg": "access denied"}, 403
        log = "Creating roles... "
        admin_role = RoleModel.find_by_name("administrators")
        if not admin_role:
            administrators = RoleModel(None, "administrators", True)
            administrators.save_to_db()

        default_admin = UserModel.find_by_username(app.config['DEFAULT_ADMIN_NAME'])
        if default_admin:
            admin_role = RoleModel.find_by_name("administrators")
            log += "Default user 'admin' already exist. Resetting admin role to "+str(admin_role.role_id)+" and password to admin. "
            default_admin.role_id = admin_role.role_id
            default_admin.password = generate_password_hash(app.config['DEFAULT_ADMIN_PASSWORD']).decode('utf-8')
            default_admin.save_to_db()
        else:
            admin_role = RoleModel.find_by_name("administrators")
            new_admin = UserModel(None, None, None, None,
                                  generate_password_hash(app.config['DEFAULT_ADMIN_PASSWORD']).decode('utf-8'),
                                  "admin",
                                  admin_role.role_id,
                                  None)
            new_admin.save_to_db()
            log += "Default user 'admin' with role "+str(admin_role.role_id)+" and password  admin created. "
        log += "Role administrators created. "

        user_role = RoleModel.find_by_name("users")
        if not user_role:
            users = RoleModel(None, "users", False)
            users.save_to_db()

        default_user = UserModel.find_by_username(app.config['DEFAULT_USER_NAME'])
        if default_user:

            user_role = RoleModel.find_by_name("users")
            default_user.role_id = user_role.role_id
            default_user.password = generate_password_hash(app.config['DEFAULT_USER_PASSWORD']).decode('utf-8')
            default_user.save_to_db()
            log += "Default user 'user' already exist. Resetting user role to "+str(user_role.role_id)+" and password to user. "
        else:

            user_role = RoleModel.find_by_name("users")
            new_user = UserModel(None, None, None, None,
                                 generate_password_hash(app.config['DEFAULT_USER_PASSWORD']).decode('utf-8')
                                 , "user",
                                 user_role.role_id
                                 , None)
            new_user.save_to_db()
            log += "Default user 'user' with role " + str(user_role.role_id) + "created. "
        log += "Role users created. "
        return {"msg": log}, 201
