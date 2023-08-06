from chalicelib.model.operation import OperationTable
from chalicelib.service.base_service import BaseService


class OperationService(BaseService):
    model = OperationTable
    update_ignore_keys = BaseService.update_ignore_keys + ("ticker", "buy")
