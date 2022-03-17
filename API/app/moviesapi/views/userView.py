from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from passlib.hash import bcrypt_sha256
from datetime import datetime, timedelta
from neomodel import db
from .. import serializers
from .. import utils
from .. import models
import time
import uuid
import json



@csrf_exempt
def signup(request):
    """This function lets the user signup (create a new account)"""
    json_data = json.loads(request.body)
    try:
        user = serializers.UserSerializer.fromJsonToUser(json_data)
    except Exception as e:
        return HttpResponseBadRequest(json.dumps({'title': str(e), 'message': 'Malformed data!'}))

    node_set = models.User.nodes.first_or_none(email = user.email)
    if node_set != None:
        return HttpResponseBadRequest(json.dumps({'title': 'email', 'message': 'Email already exists!'}))

    validate = utils.regularExpressionCheck(user.password, '^(?=.+[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})')
    if validate != True:
        return HttpResponseBadRequest(json.dumps({'title': 'password',
            'message': 'The password should contain at least one uppercase alphabetical character, one numeric character and one special character!'}))

    try:
        hash_pass = bcrypt_sha256.hash(user.password)
        if not user.profilePicture:
            path = 'moviesapi/images/profilePictures/empty.webpg'
        else:
            path = 'moviesapi/images/profilePictures/' + str(uuid.uuid4()) + '.png'
            utils.DecodeFromBase64(user.profilePicture, path)
    except Exception as e:
        return HttpResponseBadRequest(json.dumps({'title': 'image', 'message': 'The base64 string error!'}))

    try:
        with db.transaction:
            models.User(firstName=user.firstName, lastName=user.lastName, email=user.email,
                password=hash_pass, age=user.age, phoneNumber=user.phoneNumber,
                profilePicture=path, birthDate=user.birthDate).save()
    except Exception as e:
        return HttpResponseServerError(json.dumps({'title': str(e), 'message': 'The account was not created!'}))

    return HttpResponse(json.dumps({'Success' : 'The account was created successfully'}))



@csrf_exempt
def login(request):
    """This function lets the user login into his/her account"""
    json_data = json.loads(request.body)
    try:
      username = json_data['username']
      password = json_data['password']
    except Exception as e:
      return HttpResponseBadRequest(json.dumps({'title': str(e), 'message': 'Malformed data!'}))

    hash_pass = bcrypt_sha256.hash(password)
    node_set = models.User.nodes.first_or_none(email = username)
    if node_set == None:
        return HttpResponseBadRequest(json.dumps({'title': 'username', 'message': 'Wrong email!'}))
    if bcrypt_sha256.verify(password, node_set.password) != True:
        return HttpResponseBadRequest(json.dumps({'title': 'password', 'message': 'Wrong password!'}))

    user = serializers.UserSerializer.fromUserToJson(node_set)
    try :
        jwt_token = utils.generateToken(node_set.email)
        response = {
            'token': jwt_token,
            'data': user
        }
    except Exception as e:
        return HttpResponseServerError(json.dumps({'title': 'token_error', 'message': 'Could not generate token!'}))

    try :
        token_id = db.cypher_query("CREATE (t:Token { token: '" + jwt_token + "' }) RETURN ID(t)")[0][0][0]
        user_id = db.cypher_query("MATCH (u:User) where u.email='" + node_set.email + "' RETURN ID(u)")[0][0][0]
        db.cypher_query("Match(user:User) WHERE ID(user) = " + str(user_id) + " Match(token:Token) WHERE ID(token) = " + str(token_id) + " Merge (user)-[r:Authenticated{timestamp: '" + str(int(time.mktime(datetime.today().timetuple()))) + "'}]->(token)")
    except Exception as e:
        return HttpResponseServerError(json.dumps({'title': str(e), 'message': 'The token relationship was not created!'}))

    return HttpResponse(json.dumps(response))



@csrf_exempt
def refreshToken(request):
    """This function refreshes a user's token by creating a new one and removing the old token"""
    headers = request.headers
    token = utils.getTokenFromHeader(headers)
    if isinstance(token, HttpResponseBadRequest):
        return token

    try:
        result = db.cypher_query("MATCH (user:User)-[auth:Authenticated]->(token:Token{token:'" + token.token + "'}) RETURN user.email, ID(user), ID(auth)")
    except Exception as e:
        return HttpResponseServerError(json.dumps({'title': str(e), 'message': 'Database error!'}))

    try:
        email= result[0][0][0]
        user_id = result[0][0][1]
        auth_id = result[0][0][2]
        token.token = utils.generateToken(email)
        token.save();
        db.cypher_query("MATCH (u:User)-[r:Authenticated]->(t:Token) WHERE ID(r) = " + str(auth_id) + " SET r.timestamp= '" + str(int(time.mktime(datetime.today().timetuple()))) + "'")
    except Exception as e:
        return HttpResponseServerError(json.dumps({'title': str(e), 'message': 'Database error!'}))

    return HttpResponse(json.dumps({'token' : token.token}))


@csrf_exempt
def editProfile(request):
    """This function lets the user update his/her own profile"""
    headers = request.headers
    token = utils.getTokenFromHeader(headers)
    if isinstance(token, HttpResponseBadRequest):
        return token

    json_data = json.loads(request.body)
    try:
        updated_user = serializers.UserSerializer.fromJsonToUserWithoutPass(json_data)
    except Exception as e:
        return HttpResponseBadRequest(json.dumps({'title': str(e), 'message': 'Malformed data!'}))

    try:
        with db.transaction:
            result = db.cypher_query("MATCH (user:User)-[auth:Authenticated]->(token:Token) WHERE token.token = '" + token.token + "' RETURN ID(user)")
    except Exception as e:
        return HttpResponseServerError(json.dumps({'title': str(e), 'message': 'Database error!'}))

    user_id = result[0][0][0]
    try:
        string_date = str(updated_user.birthDate.month) + "/" + str(updated_user.birthDate.day) + "/" + str(updated_user.birthDate.year)
        db.cypher_query("MATCH (n:User) WHERE ID(n) = " + str(user_id) + " SET n.firstName = '" + updated_user.firstName + "', n.lastName = '" + updated_user.lastName + "', n.age = '" + str(updated_user.age) + "', n.phoneNumber = '" + updated_user.phoneNumber + "', n.profilePicture = '" + updated_user.profilePicture + "', n.birthDate = '" + string_date + "'")
    except Exception as e:
        return HttpResponseServerError(json.dumps({'title': str(e), 'message': 'Database error!'}))

    return HttpResponse(json.dumps({'Success' : 'The profile was updated'}))

@csrf_exempt
def logout(request):
    """This function lets the user log out of his/her profile"""
    headers = request.headers
    token = utils.getTokenFromHeader(headers)
    if isinstance(token, HttpResponseBadRequest):
        return token

    db.cypher_query("MATCH (t:Token) WHERE t.token = '" + token.token + "' DETACH DELETE t")

    return HttpResponse(json.dumps({'Success' : 'The token was successfully deleted!'}))
