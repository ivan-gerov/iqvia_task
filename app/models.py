from main import db
from marshmallow import fields, Schema, post_load


class Contact(db.Model):
    """Contact model"""

    __tablename__ = "contacts"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, username, first_name="", last_name=""):
        print("Making a new contact")
        self.username = username
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return f"{self.username}:{getattr(self, 'first_name', '<first_name>')} {getattr(self, 'last_name', '<last_name>')}"


db.create_all()


class ContactSchema(Schema):
    """Contact schema"""

    class Meta:
        model = Contact
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    username = fields.String(required=True)
    first_name = fields.String(required=True, data_key="first_name")
    last_name = fields.String(required=True, data_key="last_name")

    @post_load
    def make_contact(self, data, **kwargs):
        return Contact(**data)
