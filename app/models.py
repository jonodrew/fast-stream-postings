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
    id = db.Column(db.Integer, primary_key=True)
    organisation_id = db.Column(db.Text)  # this should be linked to another table
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    region_id = db.Column(db.Text)  # this should be linked to another table
    private_office = db.Column(db.Boolean, default=False)
