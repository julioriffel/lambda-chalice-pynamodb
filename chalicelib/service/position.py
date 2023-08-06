from chalicelib.model.position import PositionTable
from chalicelib.service.base_service import BaseService


class PositionService(BaseService):
    model = PositionTable
    update_ignore_keys = BaseService.update_ignore_keys + ("ticker",)
