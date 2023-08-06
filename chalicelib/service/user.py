import json

from chalicelib.model import UserTable
from chalicelib.util.auth import encode_password


class UserService(object):
    @classmethod
    def list_users(cls):
        user_ids = {}
        for item in UserTable.scan():
            if item.username not in user_ids:
                user_ids[item.username] = item.name
        return json.dumps(user_ids)

    @classmethod
    def create_user(cls, event_data):
        if password := event_data.get("password"):
            pasw = encode_password(password)

            obj = UserTable(
                username=f"{event_data.get('username')}",
                name=f"{event_data.get('name')}",
                salt=pasw.get("salt"),
                hashed=pasw.get("hashed"),
                rounds=pasw.get("rounds"),
            )
            obj.save()
        return json.dumps(obj.attribute_values, default=str)

    @classmethod
    def get_user(cls, username) -> UserTable | None:
        try:
            return UserTable.get(username)

        except UserTable.DoesNotExist as e:
            return None

    @classmethod
    def get_me(cls, username):
        me = cls.get_user(username)
        x = me.attribute_values
        x.pop("hashed")
        x.pop("rounds")
        x.pop("salt")
        return x
