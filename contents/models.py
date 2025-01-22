from datetime import datetime, timezone
from slugify import slugify
from flask import url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .settings import db


class Project(db.Model):
    __tablename__ = "projects"
    title = db.Column(db.String(255), nullable=False, unique=True)
    slug = db.Column(db.String(255), nullable=True, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.Unicode(128), nullable=True)
    link = db.Column(db.String(255), nullable=False, default="https://github.com/codewithmpia")
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    publish = db.Column(db.Boolean, default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)
        else:
            self.slug = ""

    @property
    def get_absolute_url(self):
        return url_for("project", slug=self.slug)

    def __repr__(self):
        return self.title
    

class Contact(db.Model):
    __tablename__ = "contacts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return self.name
    

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean(), default=False)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    def check_password(self, password2):
        return check_password_hash(self.password, password2)
    
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True
    
    def __str__(self):
        return self.username