from db import db


class DiscountModel(db.Model):
    __tablename__ = "discounts"
    discount_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dateFrom = db.Column(db.DateTime)
    dateTo = db.Column(db.DateTime)
    discount: db.Column(db.Integer)
