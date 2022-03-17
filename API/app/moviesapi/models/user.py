from neomodel import (
    StringProperty,
    IntegerProperty,
    DateTimeFormatProperty,
    StructuredNode,
    RelationshipTo,
)
from . import rated, authenticated

# Create your models here.

class User(StructuredNode):
    """This class is the user node"""

    firstName = StringProperty()
    lastName = StringProperty()
    email = StringProperty(unique_index=True)
    password = StringProperty()
    age = IntegerProperty()
    phoneNumber = StringProperty()
    profilePicture = StringProperty()
    birthDate = DateTimeFormatProperty(default_now=False, format='%m/%d/%Y')
    ratedMovies = RelationshipTo('.movies.Movie', 'RATED', model = rated.Rated)
    authenticated = RelationshipTo('.token.Token', 'Authenticated', model = authenticated.Authenticated)
