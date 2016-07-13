# -*- coding: utf-8 -*-

from . import db
from .models import User, Contact


def get_user_by_access_token(access_token):
    return User.query.filter_by(access_token=access_token).first()


def create_user(access_token, phone):
    user = User(access_token=access_token, phone=phone)
    db.session.add(user)
    db.session.commit()
    return user


def get_or_create_user(access_token, phone):
    user = get_user_by_access_token(access_token)
    if user:
        return (user, False)
    return (create_user(access_token, phone), True)


def sync_contacts(user_id, contacts):
    phone = [contact.phone for contact in contacts]
    friends = Contact.query.filter(Contact.friend_id == user_id,
                                   Contact.phone.in_(phone)).all()
    new_contacts = create_contacts(user_id=user_id,
                                   contacts=contacts,
                                   existing_contacts=friends)
    return new_contacts + friends


def create_contact(friend_id, name, phone):
    contact = Contact(friend_id=friend_id, name=name, phone=phone)
    db.session.add(contact)
    return contact


def create_contacts(user_id, contacts, existing_contacts):
    existing_phone = [contact.phone for contact in existing_contacts]
    new_contacts = []
    for contact in contacts:
        if contact.phone not in existing_phone:
            new = create_contact(friend_id=user_id,
                                 name=contact.name,
                                 phone=contact.phone)
            new_contacts.append(new)
    if new_contacts:
        db.session.commit()
    return new_contacts
