from neomodel import (
    StringProperty,
    StructuredNode
)
# Create your models here.

class Token(StructuredNode):
    """This class is the token node"""

    token = StringProperty()
