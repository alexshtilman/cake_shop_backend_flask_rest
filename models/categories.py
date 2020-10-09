from db import db


class CategoryModel(db.Model):
    __tablename__ = "categories"
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_en = db.Column(db.String)
    category_ru = db.Column(db.String)
    category_he = db.Column(db.String)
    category_img = db.Column(db.String)

    @classmethod
    def find_by_id(cls, category_id):
        return cls.query.filter_by(categore_id=category_id).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
