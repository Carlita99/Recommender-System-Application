from neomodel import (
    IntegerProperty,
    StructuredRel
)

# Create your models here.

class Authenticated(StructuredRel):
    """This class is the authenticated relationship node"""

    timestamp = IntegerProperty()
