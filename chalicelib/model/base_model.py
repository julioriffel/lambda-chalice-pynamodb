from pynamodb.attributes import UnicodeAttribute
from pynamodb.models import Model


class BaseModel(Model):
    uid = UnicodeAttribute(hash_key=True)
    username = UnicodeAttribute(range_key=True)
