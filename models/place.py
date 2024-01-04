#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
#from models.amenity import Amenity
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Integer,
    Float,
    Table
    )
from sqlalchemy.orm import relationship
from os import getenv

storage_type = getenv("HBNB_TYPE_STORAGE")

place_amenity = Table(
        'place_amenity',
        Base.metadata,
        Column(
            'place_id',
            String(60),
            ForeignKey('places.id'),
            primary_key=True,
            nullable=False
        ),
        Column(
            'amenity_id',
            String(60),
            ForeignKey('amenities.id'),
            primary_key=True,
            nullable=False
        )
    )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"

    city_id = Column(
        String(60),
        ForeignKey('cities.id', ondelete="CASCADE"),
        nullable=False)
    user_id = Column(
        String(60),
        ForeignKey('users.id', ondelete="CASCADE"),
        nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []


    if storage_type == 'db':

        reviews = relationship(
            "Review",
            cascade="all, delete",
            backref="place"
        )

        amenities = relationship(
            "Amenity",
            secondary="place_amenity",
            viewonly=False,
            back_populates="place_amenities"
        )
    else:

        @property
        def reviews(self):
            """ Getter attribute to retrieve cities associated with this state """
            from models import storage

            reviews = storage.all(Place)
            return [review for review in reviews.values() if review.place_id == self.id]
        
        @property
        def amenities(self):
            from models import storage  # Import DBStorage
            from models.amenity import Amenity

            amenity_objs = []
            for amenity_id in self.amenity_ids:
                amenity = storage.all(Amenity).get("Amenity." + amenity_id)
                if amenity:
                    amenity_objs.append(amenity)
            return amenity_objs
        
        @amenities.setter
        def amenities(self, amenity=None):
            '''
                Set list: amenity instances if Amenity.place_id==curr place.id
                Set by adding instance objs to amenity_ids attribute in Place
            '''
            from models import storage
            from models.amenity import Amenity
            
            if amenity:
                for amenity in storage.all(Amenity).values():
                    if amenity.place_id == self.id:
                        self.amenity_ids.append(amenity)
