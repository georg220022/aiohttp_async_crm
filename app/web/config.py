from dataclasses import dataclass
import typing
from yaml import safe_load

if typing.TYPE_CHECKING:
    from app.web.app import Application


@dataclass
class Config:
    username: str
    password: str


def setup_config(app: "Application"):
    with open("app/conf/config.yaml", "r") as file:
        raw_config = safe_load(file)

    app.config = Config(
        username=raw_config["credentials"]["username"],
        password=raw_config["credentials"]["password"],
    )
