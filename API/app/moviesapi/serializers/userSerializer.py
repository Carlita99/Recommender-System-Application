import json
from django.http import JsonResponse
from .. import models
from datetime import datetime

class UserSerializer():
    """The user serializer class"""

    def fromUserToJson(model):
        """returns a json object of type User"""
        return {
            'user': {
                'firstName': model.firstName,
                'lastName': model.lastName,
                'email': model.email,
                'age': model.age,
                'phoneNumber': model.phoneNumber,
                'profilePicture': model.profilePicture,
                'birthDate': str(model.birthDate)
            },
       }


    def toJsonArray(node_set):
        """Returns a json array containing User json objects"""
        user_dict = {}
        users_list = []
        for user in node_set:
            users_list.append(json.dumps(UserSerializer.fromUserToJson(user)))
        user_dict['users'] = users_list

        return JsonResponse(user_dict)


    def fromJsonToUser(json_data):
        """Returns a User object"""
        birth = datetime.strptime(json_data['birthDate'], '%m/%d/%Y')
        user = models.User(firstName = json_data['firstName'], lastName = json_data['lastName'],
            email = json_data['email'], password = json_data['password'], age = json_data['age'],
            phoneNumber = json_data['phoneNumber'], profilePicture = json_data['profilePicture'], birthDate = birth)
        return user

    def fromJsonToUserWithoutPass(json_data):
        """Returns a User object"""
        birth = datetime.strptime(json_data['birthDate'], '%m/%d/%Y')
        user = models.User(firstName = json_data['firstName'], lastName = json_data['lastName'],
            email = '', password = '', age = json_data['age'],
            phoneNumber = json_data['phoneNumber'], profilePicture = json_data['profilePicture'], birthDate = birth)
        return user
