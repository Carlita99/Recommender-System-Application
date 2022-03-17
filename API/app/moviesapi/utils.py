from django.http import HttpResponseBadRequest
from datetime import datetime, timedelta
from . import models
import base64
import re
import jwt
import json

def DecodeFromBase64(base64image, path):
    """This function decodes a base64 string a saves the picture in the corresponding path"""
    imgdata = base64.b64decode(base64image)
    with open(path, 'wb+') as f:
        f.write(imgdata)


def regularExpressionCheck(input_string, regexp_string):
    """This function checks if a string is valid using a certain regular expression"""
    regex = re.compile(regexp_string, re.I)
    match = regex.match(str(input_string))
    return bool(match)


def generateToken(email):
    """This function generates a token based on the user's email"""
    payload = {
        'email' : email,
        'exp': datetime.utcnow() + timedelta(seconds=20)
    }
    jwt_token = jwt.encode(payload, 'supersecretsecret', 'HS256')
    return jwt_token.decode('utf-8')


def getTokenFromHeader(headers):
    """This function makes sure that the token is valid"""
    try:
      token_value = headers['token']
    except Exception as e:
      return HttpResponseBadRequest(json.dumps({'title': str(e), 'message': 'Malformed data!'}))

    token = models.Token.nodes.first_or_none(token = token_value)
    if token == None:
        return HttpResponseBadRequest(json.dumps({'title': 'token', 'message': 'Cannot find the token!'}))

    return token
