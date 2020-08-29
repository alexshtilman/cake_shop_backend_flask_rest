import os

from flask import Flask

from flask_restful import Api
from db import db
from flasgger import Swagger
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
if os.environ.get("FLASK_ENV") == "production":
    app.config.from_object("config.ProdConfig")
else:
    app.config.from_object("config.DevConfig")

db.init_app(app)
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


template = {
    "openapi:": " 3.0.0",
    "info": {
        "title": "cake_shop",
        "description": "API",
        "contact": {
            "email": "gungam@outlook.com",
        },
        "version": app.config["API_VERSION"],
    },
    "securityDefinitions": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
}

swagger = Swagger(app, template=template)
