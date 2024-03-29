from flask import session
from flask_login import UserMixin
import requests, os

maxi_backend = os.getenv(
    "MAXIBOT_BACKEND", "http://132.226.211.117")
class User(UserMixin):
    def __init__(self, id, name, email, phone, status, platforms, access_token=None, refresh_token=None):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.status = status
        self.platforms = platforms
        self.access_token = access_token
        self.refresh_token = refresh_token

    @classmethod
    def get(cls, user_id):
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {session['access_token']}"}
        req = requests.get(f"{maxi_backend}/user/{user_id}", headers=headers)
        if req.status_code == 200:
            response = req.json()
            user = cls(**response)
            user.access_token = session["access_token"]
            user.refresh_token = session["refresh_token"]
            return user
        return None