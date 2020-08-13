from db import db

class RoleModel(db.Model):
    __tablename__ = "roles"
    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    isadmin = db.Column(db.Boolean)


    def __init__(self, role_id, name, isadmin):
        self.role_id = role_id
        self.name = name
        self.isadmin = isadmin

    @classmethod
    def find_by_id(cls, role_id):
        return cls.query.filter_by(role_id=role_id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def json(self):
        return {
            "role_id": self.role_id,
            "name": self.name,
            "isadmin": self.isadmin
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
