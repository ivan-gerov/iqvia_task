from flask import Blueprint, jsonify, request
from flask.helpers import make_response

from models import Contact, ContactSchema, db

api = Blueprint("api", __name__)


@api.route("/api/v1/contact", methods=["POST"])
def create_contact():
    """Create a contact"""
    data = request.get_json()
    contact_schema = ContactSchema()
    contact = contact_schema.load(data).create()
    result = contact_schema.dump(contact)
    return make_response(jsonify({"contact": result}), 200)


@api.route("/api/v1/contact", methods=["GET"])
def list_contacts():
    """Show a list of all contacts"""
    get_contacts = Contact.query.all()
    contacts = serialize_contact(get_contacts)
    return make_response(jsonify({"contacts": contacts}))


@api.route("/api/v1/contact/<int:id>", methods=["GET"])
def get_contact_by_id(id):
    """Return a contact by id"""
    get_contact = Contact.query.get(id)
    contact = serialize_contact(get_contact)
    return make_response(jsonify({"contact": contact}))


@api.route("/api/v1/contact/<string:username>", methods=["GET"])
def get_contact_by_username(username):
    """Return a contact by username"""
    search = "%{}%".format(username)
    get_contact = Contact.query.filter(Contact.username.like(search)).all()
    contact = serialize_contact(get_contact)
    return make_response(jsonify({"contacts": contact}))


@api.route("/api/v1/contact/<id>", methods=["PUT"])
def update_contact_by_id(id):
    """Update a contact by id"""
    data = request.get_json()
    get_contact = Contact.query.get(id)

    if data.get("first_name"):
        get_contact.first_name = data["first_name"]

    if data.get("last_name"):
        get_contact.last_name = data["last_name"]
    db.session.commit()

    contact = serialize_contact(get_contact)
    return make_response(jsonify({"contact": contact}))


@api.route("/api/v1/contact/<id>", methods=["DELETE"])
def remove_contact_by_id(id):
    """Remove a contact by id"""
    get_contact = Contact.query.get(id)
    db.session.delete(get_contact)
    db.session.commit()
    contact = serialize_contact(get_contact)
    return make_response(jsonify({"contact": contact}))


def serialize_contact(contact_obj):
    """Serializes a models.Contact object"""
    if isinstance(contact_obj, Contact):
        contact_obj = [contact_obj]
    contact_schema = ContactSchema(many=True)
    serialized_contact = contact_schema.dump(contact_obj)
    return serialized_contact
