from app import api


from resources.user import UserCreate, UserLogin, UserList, User, RefreshToken, UserLogout
from resources.home import Home
from resources.setup import Setup
from resources.role import RoleList, Role, RoleCreate

api.add_resource(Home, '/')

api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserCreate, "/register")
api.add_resource(UserList, '/users')

api.add_resource(UserLogin, '/auth')
api.add_resource(RefreshToken, '/refresh')
api.add_resource(UserLogout, '/logout')
api.add_resource(Setup, '/setup/<string:password>')

api.add_resource(RoleList, '/roles')
api.add_resource(Role, '/role/<int:role_id>')
api.add_resource(RoleCreate, '/create_role')
