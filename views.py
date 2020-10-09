from app import api


from resources.auth import UserLogin, RefreshToken, UserLogout
from resources.google import GoogleLogin, GoogleLoginCallback
from resources.user import UserCreate, UserList, User
from resources.shop import Shop_items
from models.categories import CategoryModel

from resources.home import Home
api.add_resource(Home, '/')


api.add_resource(UserLogin, '/login')
api.add_resource(RefreshToken, '/refresh')
api.add_resource(UserLogout, '/logout')

api.add_resource(GoogleLogin, '/google/login')
api.add_resource(GoogleLoginCallback, '/google/login/callback')


api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserCreate, "/register")
api.add_resource(UserList, '/users')

api.add_resource(Shop_items, '/shop_items')
