import os

class Config:
    SECRET_KEY = "super_secret_key_change_this"

    SQLALCHEMY_DATABASE_URI = "sqlite:///secure_auth.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False