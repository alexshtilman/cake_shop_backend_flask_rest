from db import db


class ShopModel(db.Model):

    __tablename__ = "shop_items"
    item_id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.category_id", ondelete="cascade"),
        nullable=False,
    )
    header_en = db.Column(db.String)
    header_ru = db.Column(db.String)
    header_he = db.Column(db.String)
    text_en = db.Column(db.String)
    text_ru = db.Column(db.String)
    text_he = db.Column(db.String)
    img = db.Column(db.String)
    min = db.Column(db.Integer)
    max = db.Column(db.Integer)
    price = db.Column(db.Float)

    def __init__(
        self,
        item_id,
        category_id,
        header_en,
        header_ru,
        header_he,
        text_en,
        text_ru,
        text_he,
        img,
        min,
        max,
        price,
    ):
        self.item_id = item_id
        self.category_id = category_id
        self.header_en = header_en
        self.header_ru = header_ru
        self.header_he = header_he
        self.text_en = text_en
        self.text_ru = text_ru
        self.text_he = text_he
        self.img = img
        self.min = min
        self.max = max
        self.price = price

    def json(self):
        return {
            "item_id": self.item_id,
            "category_id": self.category_id,
            "header_en": self.header_en,
            "header_ru": self.header_ru,
            "header_he": self.header_he,
            "text_en": self.text_en,
            "text_ru": self.text_ru,
            "img": self.img,
            "min": self.min,
            "max": self.max,
            "price": self.price,
        }

    @classmethod
    def find_by_id(cls, item_id):
        return cls.query.filter_by(item_id=item_id).first()

    @classmethod
    def find_by_category(cls, category_id):
        return cls.query.filter_by(category_id=category_id).all()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()