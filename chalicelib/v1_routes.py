from chalice import Blueprint, AuthResponse

from chalicelib.service import OperationService
from chalicelib.service import PositionService
from chalicelib.service.user import UserService
from chalicelib.util import auth

v1_routes = Blueprint(__name__)


@v1_routes.authorizer()
def jwt_auth(auth_request):
    token = auth_request.token
    decoded = auth.decode_jwt_token(token)
    return AuthResponse(routes=["*"], principal_id=decoded["sub"])


def get_authorized_username(current_request):
    return current_request.context["authorizer"]["principalId"]


@v1_routes.route("/v1/users", methods=["GET"], cors=True, authorizer=jwt_auth)
def list_users():
    return UserService.list_users()


@v1_routes.route(
    "/v1/users", methods=["POST"]
)  # , cors=True, authorizer=jwt_auth) #Is Super User
def creete_users():
    return UserService.create_user(v1_routes.current_request.json_body)


@v1_routes.route("/v1/login", methods=["POST"])
def login_post():
    body = v1_routes.current_request.json_body
    record = UserService.get_user(body["username"])
    x = auth.login(record, body["password"])
    return x


@v1_routes.route("/v1/me", methods=["GET"], cors=True, authorizer=jwt_auth)
def get_me():
    username = get_authorized_username(v1_routes.current_request)
    return UserService.get_me(username)


@v1_routes.route("/v1/operation", methods=["GET"], cors=True, authorizer=jwt_auth)
def get_operation():
    username = get_authorized_username(v1_routes.current_request)
    return OperationService.get_by_username(username)


@v1_routes.route("/v1/operation", methods=["POST"], cors=True, authorizer=jwt_auth)
def post_operation():
    username = get_authorized_username(v1_routes.current_request)
    payload = v1_routes.current_request.json_body
    return OperationService.create(payload, username)


@v1_routes.route(
    "/v1/operation/{uid}", methods=["PATCH"], cors=True, authorizer=jwt_auth
)
def patch_operation(uid):
    username = get_authorized_username(v1_routes.current_request)
    payload = v1_routes.current_request.json_body
    return OperationService.update(uid, username, payload)


@v1_routes.route(
    "/v1/operation/{uid}", methods=["DELETE"], cors=True, authorizer=jwt_auth
)
def delete_operation(uid):
    username = get_authorized_username(v1_routes.current_request)
    return OperationService.delete(uid, username)


@v1_routes.route("/v1/position", methods=["GET"], cors=True, authorizer=jwt_auth)
def get_position():
    username = get_authorized_username(v1_routes.current_request)
    return PositionService.get_by_username(username)


@v1_routes.route("/v1/position", methods=["POST"], cors=True, authorizer=jwt_auth)
def post_position():
    username = get_authorized_username(v1_routes.current_request)
    payload = v1_routes.current_request.json_body
    return PositionService.create(payload, username)


@v1_routes.route(
    "/v1/position/{uid}", methods=["PATCH"], cors=True, authorizer=jwt_auth
)
def patch_position(uid):
    username = get_authorized_username(v1_routes.current_request)
    payload = v1_routes.current_request.json_body
    return PositionService.update(uid, username, payload)


@v1_routes.route(
    "/v1/position/{uid}", methods=["DELETE"], cors=True, authorizer=jwt_auth
)
def delete_position(uid):
    username = get_authorized_username(v1_routes.current_request)
    return PositionService.delete(uid, username)
