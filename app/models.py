from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, post_load

db = SQLAlchemy()


class Contact(db.Model):
    """Contact model"""

    __tablename__ = "contact"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    username = db.Column(db.String(255))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email_addresses = db.relationship("Email", backref=db.backref("contact"))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, username, first_name="", last_name=""):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return f"{self.username}:{getattr(self, 'first_name', '<first_name>')} {getattr(self, 'last_name', '<last_name>')}"


class Email(db.Model):
    """Email model"""

    __tablename__ = "emails"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    address = db.Column(db.String(120), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, address):
        self.address = address

    def __repr__(self):
        return f"Address: {self.address} : Contact: {self.contact_id}"


class EmailSchema(Schema):
    """Email Schema"""

    class Meta:
        model = Email
        sqla_session = db.session


class ContactSchema(Schema):
    """Contact schema"""

    class Meta:
        model = Contact
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    username = fields.String(required=True)
    first_name = fields.String(required=True, data_key="first_name")
    last_name = fields.String(required=True, data_key="last_name")
    created_at = fields.DateTime()
    addresses = fields.Nested(EmailSchema)

    @post_load
    def make_contact(self, data, **kwargs):
        return Contact(**data)
