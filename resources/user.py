from flask_bcrypt import generate_password_hash
from flask_restful import Resource, reqparse
import flask_jwt_extended
from collections.abc import Iterable

from models.user import UserModel



ADMIN_REQUIRED = 'admin privileges required'


class UserCreate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="Имя пользователя обязательное поле")
    parser.add_argument('password', type=str, required=True, help="Пароль  обязательное поле")

    @flask_jwt_extended.jwt_required
    def post(self):

        identity = flask_jwt_extended.get_jwt_identity()
        if not identity["is_admin"]:
            return {'msg': ADMIN_REQUIRED}, 403
        data = UserCreate.parser.parse_args()
        if len(data['username']) < 6:
            return {"msg": "минимальная длинна имени пользователя 7 символов"}, 400
        if len(data['password']) < 6:
            return {"msg": "минимальная длинна пароля 7 символов"}, 400
        if UserModel.find_by_username(data['username']):
            return {"msg": "пользователь с таким именем уже существует"}, 400
        new_user = UserModel(None, None, None, None,
                             generate_password_hash(data['password']).decode('utf-8'),
                             data['username'],
                             data['role_id'], None)
        new_user.save_to_db()
        return {"msg": "пользователь создан", "user": new_user.json()}, 201

class UserList(Resource):

    @flask_jwt_extended.jwt_required
    def get(self):
        identity = flask_jwt_extended.get_jwt_identity()
        if not identity["is_admin"]:
            return {'msg': ADMIN_REQUIRED}, 403
        user_list = UserModel.get_all()
        if isinstance(user_list, Iterable):
            return {'users': list(map(lambda x: x.json(), user_list))}, 200
        return {'users': user_list.json()}, 200


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=int, help="user_id обязательное поле")
    @flask_jwt_extended.jwt_required
    def get(self, user_id):
        data = User.parser.parse_args()
        identity = flask_jwt_extended.get_jwt_identity()

        if user_id != identity['user_id'] and not identity["is_admin"]:
            return {'msg': ADMIN_REQUIRED}, 403

        user = UserModel.find_by_id(user_id)
        if user:
            return user.json()
        return {'msg': 'user not found'}, 404

    @flask_jwt_extended.jwt_required
    def delete(self, user_id):

        identity = flask_jwt_extended.get_jwt_identity()
        if not identity["is_admin"]:
            return {'msg': ADMIN_REQUIRED}, 403
        return {'msg': 'not jet implemented'}, 200

    @flask_jwt_extended.jwt_required
    def put(self):

        identity = flask_jwt_extended.get_jwt_identity()
        if not identity["is_admin"]:
            return {'msg': ADMIN_REQUIRED}, 403
        return {'msg': 'not jet implemented'}, 200
