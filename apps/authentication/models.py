# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy import func

from apps import db, login_manager

from apps.authentication.util import hash_pass

class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Mociones_Votos(db.Model):
    __tablename__= 'Mociones_Votos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Mocion_ID = db.Column(db.Integer,db.ForeignKey('Mociones.PIN'))
    Voto = db.Column(db.String(40))
    Nombre_Votante = db.Column(db.String(40), unique=True)
    Email_Votante = db.Column(db.String(40)  , unique=True)
    Token_Participante = db.Column(db.String(40), unique=True)
    time_date = db.Column(db.DateTime, default=func.now())
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Mociones(db.Model):
    __tablename__= 'Mociones'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PIN = db.Column(db.Integer)
    Mocion = db.Column(db.Text(500))
    Description = db.Column(db.Text(1000) , unique=False)
    Status = db.Column(db.String(20)  , unique=False)
    Results = db.Column(db.String(20),unique=False)
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}



@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None
