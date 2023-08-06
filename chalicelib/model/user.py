import os

from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute,
    BooleanAttribute,
    NumberAttribute,
    BinaryAttribute,
)


class UserTable(Model):
    class Meta(object):
        table_name = os.getenv("DB_USER_TABLE_NAME", "dev_user")
        host = os.getenv("DB_HOST", None)
        region = os.getenv("DB_REGION", "us-east-1")

    username = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    salt = BinaryAttribute()
    hashed = BinaryAttribute()
    rounds = NumberAttribute()
    is_superuser = BooleanAttribute(default=False)
