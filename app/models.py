import datetime
import random
import statistics
from typing import Dict, List, Any, Union, Set, Tuple
import sys
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from time import time
from flask import current_app, json


class Role(db.Model):
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    deliverables = db.Column(db.Text)
    specialism = db.Column(db.String)
    family = db.Column(db.String)
    organisation = db.Column(db.Text)  # this should be linked to another table

    address = db.Column(db.Text)  # this should be linked to another table



    def generate_key(self, prospective_key):
        existing_keys = self.query(Role.id).all()
        while prospective_key in existing_keys:
            pass
