from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import Pupil, Token

class TokenAuthentication(BaseBackend):

    def authenticate(self, request, username=None, password=None):
        try:
            pupil = Pupil.objects.get(id=username)
            if pupil.password == password:
                token, created = Token.objects.get_or_create(pupil=pupil)
                return token
        except Pupil.DoesNotExist:
            return None

    def get_user(self, token_key):
        try:
            token = Token.objects.get(key=token_key)
            return token.pupil
        except Token.DoesNotExist:
            return None
