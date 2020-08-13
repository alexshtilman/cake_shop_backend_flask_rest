from db import db

from models.session import SessionModel
from collections.abc import Iterable


class UserModel(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lastname = db.Column(db.String(80))
    firstname = db.Column(db.String(80))
    position = db.Column(db.String(80))
    password = db.Column(db.String(80))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.role_id"))
    username = db.Column(db.String(80))
    sessions = db.relationship(SessionModel, primaryjoin=user_id == SessionModel.user_id, lazy='dynamic')

    def __init__(self, user_id, lastname, firstname, position, password, username,  role_id,sessions):
        self.user_id = user_id
        self.lastname = lastname
        self.firstname = firstname
        self.position = position
        self.password = password
        self.username = username
        if isinstance(sessions, Iterable):
            self.sessions = sessions
        self.role_id = role_id

    def json(self):
        return {'user_id': self.user_id,
                'lastname': self.lastname,
                'firstname': self.firstname,
                'position': self.position,
                'username': self.username,
                'role_id': self.role_id
                }

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
