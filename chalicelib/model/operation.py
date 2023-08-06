import os

from pynamodb.attributes import UnicodeAttribute, NumberAttribute, BooleanAttribute

from chalicelib.model.base_model import BaseModel


class OperationTable(BaseModel):
    class Meta(object):
        table_name = os.getenv("DB_OPERATION_TABLE_NAME", "dev_operation")
        host = os.getenv("DB_HOST", None)
        region = os.getenv("DB_REGION", "us-east-1")

    date = UnicodeAttribute()
    ticker = UnicodeAttribute()
    qtd = NumberAttribute()
    price_unit = NumberAttribute()
    buy = BooleanAttribute(default=True)
