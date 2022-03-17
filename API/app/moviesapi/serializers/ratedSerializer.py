import json
from django.http import JsonResponse

class RatedSerializer():
    """The movie rated class"""

    def serializeData(model):
        """returns a json object of type Rated"""
        return {
            'rated': {
                'comment' : model.comment,
                'rating' : model.rating,
                'timestamp' : model.timestamp,
            },
       }

    def toJsonArray(node_set):
        """Returns a json array containing Rated json objects"""
        ratings_dict = {}
        rating_list = []
        for rating in node_set:
            rating_list.append(json.dumps(RatedSerializer.serializeData(rating)))
        ratings_dict['ratings'] = rating_list

        return JsonResponse(ratings_dict)
