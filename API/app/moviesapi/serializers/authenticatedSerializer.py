import json
from django.http import JsonResponse

class AuthenticatedSerializer():
    """The movie rated class"""

    def serializeData(model):
        """returns a json object of type Authenticated"""
        return {
            'authenticated': {
                'timestamp' : model.timestamp,
            },
       }

    def toJsonArray(node_set):
        """Returns a json array containing Authenticated json objects"""
        auth_dict = {}
        auth_list = []
        for auth in node_set:
            auth_list.append(json.dumps(RatedSerializer.serializeData(auth)))
        auth_dict['authentications'] = auth_list

        return JsonResponse(auth_dict)
