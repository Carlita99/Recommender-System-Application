from neomodel import (
    StringProperty,
    IntegerProperty,
    DateTimeFormatProperty,
    ArrayProperty,
    BooleanProperty,
    StructuredNode,
    RelationshipFrom,
)
from . import rated


# Create your models here.

class Movie(StructuredNode):
    """This class is the movie node"""

    posterURL = StringProperty()
    releaseDate = DateTimeFormatProperty(default_now=False, format='%m/%d/%Y')
    genres = ArrayProperty()
    parentalControl = BooleanProperty()
    runtime = IntegerProperty()
    description = StringProperty()
    countries = ArrayProperty()
    title = StringProperty()
    imdbLink = StringProperty()
    usersRated = RelationshipFrom('.user.User', 'RATED', model = rated.Rated)
