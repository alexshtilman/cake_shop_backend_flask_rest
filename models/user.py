from db import db


class UserModel(db.Model):
    __tablename__ = "users"
    unique_id = db.Column(db.String, unique=True, primary_key=True)
    password = db.Column(db.String(80))
    is_admin = db.Column(db.BOOLEAN)
    users_name = db.Column(db.String(80))
    users_email = db.Column(db.String, nullable=False)
    profile_pic = db.Column(db.String)

    def __init__(self, unique_id, password, is_admin, users_name, users_email, profile_pic):
        self.unique_id = unique_id
        self.password = password
        self.is_admin = is_admin
        self.users_name = users_name
        self.users_email = users_email
        self.profile_pic = profile_pic

    def json(self):
        return {
                'unique_id': self.unique_id,
                'password': self.password,
                'is_admin': self.is_admin,
                'users_name': self.users_name,
                'users_email': self.users_email,
                'profile_pic': self.profile_pic
                }

    @classmethod
    def find_by_username(cls, users_name):
        return cls.query.filter_by(username=users_name).first()

    @classmethod
    def find_by_id(cls, unique_id):
        return cls.query.filter_by(unique_id=unique_id).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
