import os

from pynamodb.attributes import UnicodeAttribute, NumberAttribute, BooleanAttribute

from chalicelib.model.base_model import BaseModel


class PositionTable(BaseModel):
    class Meta(object):
        table_name = os.getenv("DB_POSITION_TABLE_NAME", "dev_position")
        host = os.getenv("DB_HOST", None)
        region = os.getenv("DB_REGION", "us-east-1")

    ticker = UnicodeAttribute()
    qtd = NumberAttribute()
    price_unit = NumberAttribute()
