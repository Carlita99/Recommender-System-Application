from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest
from neomodel import db
from .. import models
from ..  import serializers
import json



@csrf_exempt
def getMostRecentMovies(request):
    """This function returns the most recent movies"""
    json_data = json.loads(request.body)
    try:
      start = json_data['start']
      limit = json_data['limit']
    except Exception as e:
        return HttpResponseBadRequest(json.dumps({'title': str(e), 'message': 'Malformed data!'}))

    result = db.cypher_query('MATCH (m:Movie) WHERE EXISTS(m.releaseDate) RETURN m, ID(m) ORDER BY m.releaseDate DESC SKIP ' + str(start) + ' LIMIT ' + str(limit))
    movies = []
    for res in result[0]:
        movie = serializers.MovieSerializer.fromJsonToMovie(res[0])
        movies.append(serializers.MovieSerializer.fromMovieToJson(movie, getMovieAverageRating(res[1]), res[1]))

    return HttpResponse(json.dumps({'mostRecentMovies' : movies}))



@csrf_exempt
def getMostPopularMovies(request):
    """This function returns the most popular movies"""
    json_data = json.loads(request.body)
    try:
      start = json_data['start']
      limit = json_data['limit']
    except Exception as e:
        return HttpResponseBadRequest(json.dumps({'title': str(e), 'message': 'Malformed data!'}))

    result = db.cypher_query('MATCH (u:User)-[r:Rated]->(m:Movie) RETURN AVG(r.rating) as average, m, ID(m) ORDER BY average DESC SKIP ' + str(start) + ' LIMIT ' + str(limit))
    movies = []
    for res in result[0]:
        movie = serializers.MovieSerializer.fromJsonToMovie(res[1])
        movies.append(serializers.MovieSerializer.fromMovieToJson(movie, res[0], res[2]))

    return HttpResponse(json.dumps({'mostPopularMovies' : movies}))



@csrf_exempt
def getMovieAverageRating(movie_id):
    """This function returns the average of a movie given its id"""
    result = db.cypher_query('MATCH (u:User)-[r:Rated]->(m:Movie) WHERE ID(m) = ' + str(movie_id) + ' RETURN AVG(r.rating) as average')
    return result[0][0][0]
