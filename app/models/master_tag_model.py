from app import db


class MasterTag(db.Model):
    __tablename__ = "master_tag"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    web_id = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    path = db.Column(db.String(150), nullable=False)
    descriptor = db.Column(db.String(150), nullable=True)
    point_class = db.Column(db.String(15), nullable=True)
    point_type = db.Column(db.String(15), nullable=True)
    digital_set_name = db.Column(db.String(150), nullable=True)
    engineering_units = db.Column(db.String(15), nullable=True)
    span = db.Column(db.Integer, nullable=True)
    zero = db.Column(db.Integer, nullable=True)
    step = db.Column(db.Boolean, nullable=True)
    future = db.Column(db.Boolean, nullable=True)
    display_digits = db.Column(db.Integer, nullable=False)
    tag_values = db.relationship("ValueTag", backref="master_tag", lazy=True)

    def __repr__(self):
        return f"<MasterTag {self}>"
