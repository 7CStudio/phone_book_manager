# -*- coding: utf-8 -*-

from sqlalchemy.sql import func
from sqlalchemy.schema import Index

from . import db


class TimeStampMixin(object):
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(),
                           onupdate=func.utcnow(), nullable=False)


class User(db.Model, TimeStampMixin):
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(80), unique=True,
                             index=True)
    phone = db.Column(db.String(15), unique=True,
                      index=True)


class Contact(db.Model, TimeStampMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    phone = db.Column(db.String(15), index=True)

    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    friend = db.relationship('User',
                             backref=db.backref('contacts', lazy='dynamic'),
                             foreign_keys=[friend_id])

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship('User', foreign_keys=[user_id])

    __table_args__ = (Index('friend_id_phone', "friend_id", "phone"), )
