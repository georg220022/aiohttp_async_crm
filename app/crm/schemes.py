#
from marshmallow import Schema, fields

from app.web.schemas import OkResponseSchema


class UserAddSchema(Schema):
    email = fields.Str(required=True)


class UserSchema(UserAddSchema):
    # В моделях id хранится как id_
    id = fields.UUID(required=True, attribute="id_")


class UserGetRequestSchema(Schema):
    id = fields.UUID(required=True)


class UserGetSchema(Schema):
    # Nested - вложенность
    user = fields.Nested(UserSchema)


class UserGetListSchema(Schema):
    user = fields.Nested(UserSchema)


class GetUserResponseSchema(OkResponseSchema):
    data = fields.Nested(UserGetSchema)


class ListUserSchema(Schema):
    users = fields.Nested(UserSchema, many=True)


class ListResponseSchema(OkResponseSchema):
    data = fields.Nested(ListUserSchema)
