import json
from django.http import JsonResponse
from .. import models

class TokenSerializer():
    """The token serializer class"""

    def fromTokenToJson(model):
        """returns a json object of type Token"""
        return {
            'token': {
                'token': model.token,
            },
       }


    def toJsonArray(node_set):
        """Returns a json array containing Token json objects"""
        token_dict = {}
        token_list = []
        for token in node_set:
            token_list.append(json.dumps(UserSerializer.fromUserToJson(token)))
        token_dict['tokens'] = token_list

        return JsonResponse(token_dict)


    def fromJsonToToken(json_data):
        """Returns a token object"""
        token = models.Token(token = json_data['token'])
        return token
