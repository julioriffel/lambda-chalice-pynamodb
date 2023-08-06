import os
from chalice import Chalice

from chalicelib.model.operation import OperationTable
from chalicelib.model.position import PositionTable
from chalicelib.model.user import UserTable
from chalicelib.v1_routes import v1_routes

import logging

for db_instance in [UserTable, OperationTable, PositionTable]:
    if not db_instance.exists():
        db_instance.create_table(
            read_capacity_units=1, write_capacity_units=1, wait=True
        )

app = Chalice(app_name="api_backend")
app.register_blueprint(v1_routes)

app.debug = os.getenv("BACKEND_DEBUG", False)
log_level = logging.DEBUG if app.debug else logging.INFO
app.log.setLevel(log_level)
