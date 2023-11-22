#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
import shlex
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models
from models.city import City


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    cities = relationship("City", cascade='all, delete, delete-orphan',
                          backref="state")

    @property
    def cities(self):
        var = models.storage.all()
        liste = []
        result = []
        for key in var:
            city = key.replace('.', ' ')
            city = shlex.split(city)
            if (city[0] == 'City'):
                liste.append(var[key])
        for element in liste:
            if (elem.state_id == self.id):
                result.append(element)
        return (result)
