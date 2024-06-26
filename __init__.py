#!/usr/bin/python3
"""Selects between FileStorage and DBStorage instance for your application"""
from os import getenv

from models.base_model import BaseModel
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


""" Environment variable 'HBNB_TYPE_STORAGE' acts as a toggle
"""

if getenv('HBNB_TYPE_STORAGE') == "db":

    from models.engine.db_storage import DBStorage
    storage = DBStorage()
    storage.reload()

else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
      storage.reload()
