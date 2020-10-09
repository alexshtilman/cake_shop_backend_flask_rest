from flask_bcrypt import generate_password_hash
from flask_restful import Resource, reqparse
import flask_jwt_extended
from collections.abc import Iterable

from models.shop import ShopModel


class Shop_items(Resource):
    def get(self):
        #identity = flask_jwt_extended.get_jwt_identity()
        shop_items = ShopModel.get_all()
        if not shop_items:
            return {"shop_items": []}, 200
        if isinstance(shop_items, Iterable):
            return {'sessions': list(map(lambda x: x.json(), shop_items))}, 200
        return {"shop_items": shop_items.json()}, 200
