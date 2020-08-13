from collections import Iterable

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse

from models.role import RoleModel


class Role(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=False, help="У роли должно быть имя")
    parser.add_argument('isadmin', type=bool, required=False, help="У роли должно быть имя")
    # TODO
    @jwt_required
    def get(self, role_id):
        """Получить данные роли
            ---
                tags:
                    - Roles
                security:
                    - Bearer:
                        type: apiKey
                        name: Authorization
                        in: header
                parameters:
                 - in: path
                   name: role_id
                   type: integer
                   required: true
                responses:
                    '200':
                        description: roles { roles }
                    '400':
                        description: admin privileges required
                    '401':
                        description: Authorization information is missing or invalid.
                    '404':
                        description: A user with the specified ID was not found.
                    '5XX':
                        description: Unexpected error.
        """
        identity = get_jwt_identity()
        if not identity['is_admin']:
            return {'msg': 'admin privileges required'}, 403
        role = RoleModel.find_by_id(role_id)
        if not role:
            return {'msg': 'role not found'}, 404
        return {"role": role.json()}, 200

    # TODO
    @jwt_required
    def delete(self, role_id):
        """Удалить роль
            ---
                tags:
                    - Roles
                security:
                    - Bearer:
                        type: apiKey
                        name: Authorization
                        in: header
                parameters:
                 - in: path
                   name: role_id
                   type: integer
                   required: true
                responses:
                    '200':
                        description: roles { roles }
                    '400':
                        description: admin privileges required
                    '401':
                        description: Authorization information is missing or invalid.
                    '404':
                        description: A user with the specified ID was not found.
                    '5XX':
                        description: Unexpected error.
        """
        identity = get_jwt_identity()
        if not identity['is_admin']:
            return {'msg': 'admin privileges required'}, 403

        role = RoleModel.find_by_id(role_id)
        if not role:
            return {'msg': 'role not found'}, 404
        if role.name == "users" or role.name == "administrators":
            return {'msg': 'editing default roles is not allowed'}, 403
        role.delete_from_db()
        return {'msg': 'role deleted'}, 200

    # TODO
    @jwt_required
    def put(self, role_id):
        """Обновить данные роли
            ---
                tags:
                    - Roles
                security:
                    - Bearer:
                        type: apiKey
                        name: Authorization
                        in: header
                parameters:
                 - in: path
                   name: role_id
                   type: integer
                   required: true
                 - name: body
                   in: body
                   required: true
                   properties:
                    name:
                     type: string
                    isadmin:
                      type: boolean
                responses:
                    '200':
                        description: roles { roles }
                    '400':
                        description: admin privileges required
                    '401':
                        description: Authorization information is missing or invalid.
                    '404':
                        description: role not found by role_id.
                    '5XX':
                        description: Unexpected error.
        """
        identity = get_jwt_identity()
        if not identity['is_admin']:
            return {'msg': 'admin privileges required'}, 403

        role = RoleModel.find_by_id(role_id)
        if not role:
            return {'msg': 'role not found'}, 404
        if role.name == "users" or role.name == "administrators":
            return {'msg': 'editing default roles is not allowed'}, 403

        data_args = Role.parser.parse_args()
        if data_args['name'] == "users" or data_args['name'] == "administrators":
            return {'msg': 'editing default roles is not allowed'}, 403
        if data_args['name']:
            role.name = data_args['name']
        if data_args['isadmin']:
            role.isadmin = data_args['isadmin']
        role.save_to_db()
        return {"msg": "role updated", "role": role.json()}, 200

class RoleList(Resource):
    @jwt_required
    def get(self):
        """Получить список всех ролей
            ---
                tags:
                    - Roles
                security:
                    - Bearer:
                        type: apiKey
                        name: Authorization
                        in: header
                responses:
                    '200':
                        description: roles { roles }
                    '400':
                        description: admin privileges required
                    '401':
                        description: Authorization information is missing or invalid.
                    '404':
                        description: A user with the specified ID was not found.
                    '5XX':
                        description: Unexpected error.
        """
        identity = get_jwt_identity()
        if not identity['is_admin']:
            return {'msg': 'admin privileges required', 'roles': []}, 403
        roles_list = RoleModel.get_all()
        if isinstance(roles_list, Iterable):
            return {'roles': list(map(lambda x: x.json(), roles_list))}
        return {'roles': roles_list.json()}, 200


class RoleCreate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="У роли должно быть имя")
    parser.add_argument('isadmin', type=bool, required=True, help="У роли должно быть имя")
    @jwt_required
    def post(self):
        """Создать роль
            ---
                tags:
                    - Roles
                security:
                    - Bearer:
                        type: apiKey
                        name: Authorization
                        in: header
                parameters:
                 - name: body
                   in: body
                   required: true
                   properties:
                    name:
                     type: string
                    isadmin:
                      type: boolean
                responses:
                    '200':
                        description: roles { roles }
                    '400':
                        description: admin privileges required
                    '401':
                        description: Authorization information is missing or invalid.
                    '404':
                        description: A user with the specified ID was not found.
                    '5XX':
                        description: Unexpected error.
                """

        identity = get_jwt_identity()
        if not identity['is_admin']:
            return {'msg': 'admin privileges required', 'roles': []}, 403
        data_args = RoleCreate.parser.parse_args()
        find_role = RoleModel.find_by_name(data_args['name'])
        if find_role:
            return {"msg": "role already exist"}, 200
        new_role = RoleModel(None, data_args['name'],  data_args['isadmin'])
        new_role.save_to_db()
        return {"msg": "role created", "role": new_role.json()}, 201
