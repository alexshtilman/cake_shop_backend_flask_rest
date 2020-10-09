from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_required,
                                get_jwt_identity,
                                jwt_refresh_token_required,
                                get_raw_jwt)
from flask_bcrypt import check_password_hash
from blacklist import BLACKLIST

from models.user import UserModel


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('users_email', type=str, required=True, help="Имя пользователя обязательное поле")
    parser.add_argument('password', type=str, required=True, help="Пароль  обязательное поле")

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        user = UserModel.find_by_username(data['users_email'])
        if user and check_password_hash(user.password, data['password']):

            access_token = create_access_token(identity={'unique_id': user.unique_id,
                                                         'is_admin': user.is_admin,
                                                         'users_name': user.users_name,
                                                         'users_email': user.users_email,
                                                         'profile_pic': user.profile_pic
                                                         }, fresh=True)
            refresh_token = create_refresh_token(user.unique_id)
            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200
        return {'msg': "invalid credentials!"}, 404


class RefreshToken(Resource):
    @jwt_refresh_token_required
    def post(self):

        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200


class UserLogout(Resource):
    @jwt_required
    def delete(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {'msg': 'logout successfully'}, 200
