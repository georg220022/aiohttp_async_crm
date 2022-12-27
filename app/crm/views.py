import uuid
from app.crm.models import User
from app.crm.schemes import (
    GetUserResponseSchema,
    ListResponseSchema,
    UserAddSchema,
    UserGetRequestSchema,
    UserSchema,
    # UserGetSchema,
    # UserSchema,
)
from app.web.app import View

# from aiohttp.web_response import json_response
from app.web.utils import check_basic_auth, json_response
from aiohttp.web_exceptions import HTTPNotFound, HTTPUnauthorized, HTTPForbidden
from aiohttp_apispec import docs, request_schema, response_schema, querystring_schema

from app.web.schemas import OkResponseSchema


class AddUserView(View):
    @docs(tags=["crm"], summary="Add new user", description="Add new user to DB")
    @request_schema(UserAddSchema)
    @response_schema(OkResponseSchema, 200)
    async def post(self):
        print(self.request.app.config.username)
        data = self.request["data"]  # await self.request.json()
        user = User(email=data["email"], id_=uuid.uuid4())
        await self.request.app.crm_accessor.add_user(user)
        return json_response()  # data=dict(status="ok")


class ListUserView(View):
    @docs(tags=["crm"], summary="List users", description="Get List users from DB")
    @response_schema(ListResponseSchema, 200)
    async def get(self):
        if not self.request.headers.get("Authorization"):
            raise HTTPUnauthorized
        if not check_basic_auth(
            self.request.headers["Authorization"],
            username=self.request.app.config.username,
            password=self.request.app.config.password,
        ):
            raise HTTPForbidden
        users = await self.request.app.crm_accessor.list_users()
        raw_users = [
            UserSchema.dump(user) for user in users
        ]  # dict(email=user.email, id_=str(user.id_))
        return json_response(data=dict(users=raw_users))


class GetUserView(View):
    @docs(tags=["crm"], summary="Get user", description="Get user by id")
    @querystring_schema(UserGetRequestSchema)
    @response_schema(GetUserResponseSchema, 200)
    async def get(self):
        user_id = self.request.query["id"]
        user = await self.request.app.crm_accessor.get_user(uuid.UUID(user_id))
        if user:
            return json_response(
                data=dict(
                    user=UserSchema.dump(user)
                )  # dict(email=user.email, id=str(user.id_))
            )
        raise HTTPNotFound
