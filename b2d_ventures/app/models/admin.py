from django.db import models
from .user import User


class Admin(User):
    permission = models.TextField(blank=True)
