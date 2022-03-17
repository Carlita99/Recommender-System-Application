from neomodel import (
    StringProperty,
    IntegerProperty,
    FloatProperty,
    StructuredRel
)

# Create your models here.

class Rated(StructuredRel):
    """This class is the rated relationship node"""

    comment = StringProperty()
    rating = FloatProperty()
    timestamp = IntegerProperty()
