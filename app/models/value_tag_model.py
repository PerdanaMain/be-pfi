from app import db
from app.models.master_tag_model import MasterTag


class ValueTag(db.Model):
    __tablename__ = "value_tag"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    tag_id = db.Column(
        db.BigInteger, db.ForeignKey(MasterTag.id, ondelete="CASCADE"), nullable=False
    )
    time_stamp = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.Float, nullable=False)
    units_abbreviation = db.Column(db.String(15), nullable=False)
    good = db.Column(db.Boolean, nullable=False)
    questionable = db.Column(db.Boolean, nullable=False)
    substituted = db.Column(db.Boolean, nullable=False)
    annotated = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"<ValueTag {self}>"
