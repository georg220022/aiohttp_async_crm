import typing


if typing.TYPE_CHECKING:
    from aiohttp.web_app import Application


def setup_routes(app: "Application"):
    from app.crm.views import GetUserView
    from app.crm.views import ListUserView
    from app.crm.views import AddUserView

    app.router.add_view("/add_user", AddUserView)
    app.router.add_view("/list_users", ListUserView)
    app.router.add_view("/get_user", GetUserView)
