from flask_bcrypt import check_password_hash, generate_password_hash
from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_required,
                                get_jwt_identity,
                                jwt_refresh_token_required,
                                get_raw_jwt)
from collections.abc import Iterable

from models.user import UserModel
from models.role import RoleModel

from blacklist import BLACKLIST

ADMIN_REQUIRED = 'admin privileges required'

class UserCreate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="Имя пользователя обязательное поле")
    parser.add_argument('password', type=str, required=True, help="Пароль  обязательное поле")
    parser.add_argument('role_id', type=int, required=True, help="Айди роли  обязательное поле")

    @jwt_required
    def post(self):
        """Создать пользователя
                ---
                    tags:
                        - Users
                    summary: Gets the account billing info
                    security:
                        - Bearer:
                            type: apiKey
                            name: Authorization
                            in: header
                    parameters:
                        - name: body
                          in: body
                          required: true
                          schema:
                            id: User
                            required:
                             - username
                             - password
                             - role_id
                            properties:
                             username:
                              type: string
                              minimum: 7
                              required: true
                              description: имя пользователя
                             password:
                              type: string
                              required: true
                              minimum: 7
                              description: пароль
                             role_id:
                              type: integer
                              required: true
                              description: айди роли
                             firstname:
                              type: string
                              required: false
                              description: имя
                             lastname:
                              type: string
                              required: false
                              description: фамилия
                             position:
                              type: string
                              required: false
                              description: должность
                    responses:
                        '200':
                            description: OK
                        '401':
                            description: Not authenticated
                        '403':
                            description: Access token does not have the required scope
        """
        identity = get_jwt_identity()
        if not identity["is_admin"]:
            return {'msg': ADMIN_REQUIRED}, 403
        data = UserCreate.parser.parse_args()
        if len(data['username']) < 6:
            return {"msg": "минимальная длинна имени пользователя 7 символов"}, 400
        if len(data['password']) < 6:
            return {"msg": "минимальная длинна пароля 7 символов"}, 400
        if UserModel.find_by_username(data['username']):
            return {"msg": "пользователь с таким именем уже существует"}, 400
        if not RoleModel.find_by_id(data['role_id']):
            return {"msg": "роли с таким айди не существует"}, 400
        new_user = UserModel(None, None, None, None,
                             generate_password_hash(data['password']).decode('utf-8'),
                             data['username'],
                             data['role_id'], None)
        new_user.save_to_db()
        return {"msg": "пользователь создан", "user": new_user.json()}, 201


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="Имя пользователя обязательное поле")
    parser.add_argument('password', type=str, required=True, help="Пароль  обязательное поле")

    @classmethod
    def post(cls):
        """Получение access_token, refresh_token по username, password
            ---
                        tags:
                            - Authorization
                        parameters:
                             - name: body
                               in: body
                               required: true
                               schema:
                                 id: Auth
                                 required:
                                   - username
                                   - password
                                 properties:
                                   username:
                                     type: string
                                     required: true
                                     description: имя пользователя
                                   password:
                                     type: string
                                     required: true
                                     description: пароль
                        responses:
                            '200':
                              description: OK
                            '400':
                              description: Bad request. User ID must be an integer and larger than 0.
                            '401':
                              description: Authorization information is missing or invalid.
                            '404':
                              description: A user with the specified ID was not found.
                            '5XX':
                              description: Unexpected error.
                """
        # $ref: '#/definitions/Auth'
        data = cls.parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and check_password_hash(user.password, data['password']):
            role = RoleModel.find_by_id(user.role_id)
            access_token = create_access_token(identity={'user_id': user.user_id,
                                                         'is_admin': role.isadmin}, fresh=True)
            refresh_token = create_refresh_token(user.user_id)
            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200
        return {'msg': "invalid credentials!"}, 404


class RefreshToken(Resource):
    @jwt_refresh_token_required
    def post(self):
        """Получение access_token на основании refresh_token
            ---
             tags:
              - Authorization
             security:
                - Bearer:
                    type: apiKey
                    name: Authorization
                    in: header
             responses:
              '200':
                description: OK
              '4XX':
                description: Signature verification failed
              '5XX':
                description: Unexpected error.
        """
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200


class UserLogout(Resource):
    @jwt_required
    def delete(self):
        """Выход из системы с удалением access_token
            ---
                tags:
                    - Authorization
                security:
                    - Bearer:
                        type: apiKey
                        name: Authorization
                        in: header
                responses:
                    '200':
                      description: logout successfully
                    '400':
                      description: Bad request. User ID must be an integer and larger than 0.
                    '401':
                      description: Authorization information is missing or invalid.
                    '404':
                      description: A user with the specified ID was not found.
                    '5XX':
                      description: Unexpected error.
        """

        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {'msg': 'logout successfully'}, 200


class UserList(Resource):

    @jwt_required
    def get(self):
        """Список пользователей
            ---
                tags:
                    - Users
                security:
                    - Bearer:
                        type: apiKey
                        name: Authorization
                        in: header
                responses:
                    '200':
                      description: OK
                    '400':
                      description: Bad request. User ID must be an integer and larger than 0.
                    '401':
                      description: Authorization information is missing or invalid.
                    '404':
                      description: A user with the specified ID was not found.
                    '5XX':
                      description: Unexpected error.
        """
        identity = get_jwt_identity()
        if not identity["is_admin"]:
            return {'msg': ADMIN_REQUIRED}, 403
        user_list = UserModel.get_all()
        if isinstance(user_list, Iterable):
            return {'users': list(map(lambda x: x.json(), user_list))}, 200
        return {'users': user_list.json()}, 200


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=int, help="user_id обязательное поле")

    @jwt_required
    def get(self, user_id):
        """Информация о пользователе
            ---
                tags:
                    - Users
                parameters:
                    - in: path
                      name: user_id
                      schema:
                        type: integer
                      required: true
                      description: айди пользователя
                security:
                    - Bearer:
                        type: apiKey
                        name: Authorization
                        in: header
                responses:
                    '200':
                      description: OK
                    '400':
                      description: Bad request. User ID must be an integer and larger than 0.
                    '401':
                      description: Authorization information is missing or invalid.
                    '404':
                      description: A user with the specified ID was not found.
                    '5XX':
                      description: Unexpected error.
        """
        data = User.parser.parse_args()
        identity = get_jwt_identity()

        if user_id != identity['user_id'] and not identity["is_admin"]:
            return {'msg': ADMIN_REQUIRED}, 403

        user = UserModel.find_by_id(user_id)
        if user:
            return user.json()
        return {'msg': 'user not found'}, 404

    @jwt_required
    def delete(self, user_id):
        """Удалить пользователя
            ---
                tags:
                    - Users
                security:
                    - Bearer:
                        type: apiKey
                        name: Authorization
                        in: header
                parameters:
                    - name: path
                      in: path
                      name: user_id
                      schema:
                        type: integer
                      required: true

                responses:
                    '200':
                      description: OK
                    '400':
                      description: Bad request. User ID must be an integer and larger than 0.
                    '401':
                      description: Authorization information is missing or invalid.
                    '404':
                      description: A user with the specified ID was not found.
                    '5XX':
                      description: Unexpected error.
                        """
        identity = get_jwt_identity()
        if not identity["is_admin"]:
            return {'msg': ADMIN_REQUIRED}, 403

        #TODO
        #delete all datasets
        #delete all from sequence by user_id
        #delete all sessions
        return {'msg': 'not jet implemented'}, 200

    @jwt_required
    def put(self):
        """Изменить данные пользователя
            ---
                tags:
                    - Users
                security:
                    - Bearer:
                        type: apiKey
                        name: Authorization
                        in: header
                parameters:
                    - name: path
                      in: path
                      name: user_id
                      schema:
                        type: integer
                      required: true
                    - name: body
                      in: body
                      required: true
                      schema:
                        id: UserPut
                        properties:
                         username:
                          type: string
                          minimum: 7
                          required: false
                          description: имя пользователя
                         password:
                          type: string
                          required: false
                          minimum: 7
                          description: пароль
                         role_id:
                          type: integer
                          required: false
                          description: айди роли
                         firstname:
                          type: string
                          required: false
                          description: имя
                         lastname:
                          type: string
                          required: false
                          description: фамилия
                         position:
                          type: string
                          required: false
                          description: должность

                responses:
                    '200':
                      description: OK
                    '400':
                      description: Bad request. User ID must be an integer and larger than 0.
                    '401':
                      description: Authorization information is missing or invalid.
                    '404':
                      description: A user with the specified ID was not found.
                    '5XX':
                      description: Unexpected error.
                        """
        identity = get_jwt_identity()
        if not identity["is_admin"]:
            return {'msg': ADMIN_REQUIRED}, 403
        return {'msg': 'not jet implemented'}, 200
