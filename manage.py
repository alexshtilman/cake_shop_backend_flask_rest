import os

from flask import Flask
from db import db
import views
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# this file is only used to store db structure

app = Flask(__name__)

if os.environ.get("FLASK_ENV") == "production":
    app.config.from_object("config.ProdConfig")
else:
    app.config.from_object("config.DevConfig")

db.init_app(app)

migrate = Migrate(app, db)  # Initializing migrate.
manager = Manager(app)
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()
