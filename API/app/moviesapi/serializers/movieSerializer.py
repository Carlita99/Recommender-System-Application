import json
from django.http import JsonResponse
from .. import models
from datetime import datetime

class MovieSerializer():
    """The movie serializer class"""

    def fromMovieToJson(model, avgRating, movie_id):
        """returns a json object of type Movie"""
        return {
            'movie': {
                'id': movie_id,
                'posterURL': model.posterURL,
                'releaseDate': str(model.releaseDate),
                'genres': model.genres,
                'parentalControl': model.parentalControl,
                'runtime': model.runtime,
                'description': model.description,
                'countries': model.countries,
                'title': model.title,
                'imdbLink': model.imdbLink
            },
            'averageRating' : avgRating
       }

    def toJsonArray(node_set):
        """Returns a json array containing Movie json objects"""
        movie_dict = {}
        movies_list = []
        for movie in node_set:
            movies_list.append(MovieSerializer.fromMovieToJson(movie))
        movie_dict['movies'] = movies_list

        return JsonResponse(movie_dict)

    def fromJsonToMovie(json_data):
        """Returns a Movie object"""
        release = datetime.strptime(json_data['releaseDate'], '%m/%d/%Y')
        movie = models.Movie(posterURL = json_data['posterURL'], releaseDate = release,
            genres = json_data['genres'], parentalControl = json_data['parentalControl'], runtime = json_data['runtime'],
            description = json_data['description'], countries = json_data['countries'], title = json_data['title'], imdbLink = json_data['imdbLink'])
        return movie
