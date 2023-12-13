from typing import Callable, Iterator
from src.controllers import home, gamedays, game_day
from src.templates import render_templates


def app(environ: dict, start_response: Callable):
    path: str = environ.get("PATH_INFO")

    if path.endswith("/"):
        path = path[:-1]

    if path == "" or path == "/home":
        data: str = home(environ)

    elif path == "/gamedays":
        data: str = gamedays(environ)

    elif path == "/randombetlist" or path == "/randombetlist/check":
        data: str = game_day(environ)

    else:
        data: str = render_templates("src/views/404.html")

    data_in_bytes: bytes = data.encode("utf-8")

    start_response(
        "200 OK",
        [
            ("Content-Type", "text/html"),
            ("Content-Length", str(len(data_in_bytes)))
        ]
    )

    return iter([data_in_bytes])
