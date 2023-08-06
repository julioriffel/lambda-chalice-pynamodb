import json
import uuid

from chalice import NotFoundError
from pynamodb.exceptions import DoesNotExist

from chalicelib.model.base_model import BaseModel


class BaseService(object):
    model: BaseModel
    update_ignore_keys = ("uid",)

    @classmethod
    def clean_payload(cls, payload) -> dict:
        keys = list(payload.keys())
        for key in keys:
            if key not in cls.model.get_attributes():
                payload.pop(key, None)
        return payload

    @classmethod
    def get_uid_username(cls, uid, username, raise_exp=False):
        try:
            item = cls.model.get(uid, username)
        except DoesNotExist:
            item = None
            if raise_exp:
                raise NotFoundError
        return item

    @classmethod
    def create(cls, payload: dict, username: str):
        if id not in payload:
            payload["uid"] = str(uuid.uuid4())
        payload = cls.clean_payload(payload)
        i = cls.model(**payload, username=username)
        i.save()
        return i.attribute_values

    @classmethod
    def get_by_username(cls, username: str):
        events = []
        for event in cls.model.scan(cls.model.username == username):
            events.append(event.attribute_values)
        return json.dumps(events)

    @classmethod
    def delete(cls, uid, username):
        event = cls.get_uid_username(uid, username, True)
        if event:
            event.delete()

    @classmethod
    def update(cls, uid, username, payload: dict):
        item = cls.get_uid_username(uid, username, True)
        for key in cls.update_ignore_keys:
            payload.pop(key, None)
        payload = cls.clean_payload(payload)
        payload["username"] = username
        if item:
            for key, val in payload.items():
                setattr(item, key, val)
            item.save()
            return item.attribute_values
