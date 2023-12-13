from typing import Callable, Iterator

from src.controller import home, add_product, error404, shop, shopping_cart, add_product_cart, cart


def app(environ: dict, start_response: Callable) -> Iterator:
    path: str = environ.get("PATH_INFO")
    headers: list[tuple[str, str]] = [
        ("Content-Type", "text/html")
    ]

    if path.endswith("/"):
        path = path[:-1]

    if path == "" or path == "/home":
        data: str = home()
    elif path == "/product/db/add":
        data: str = add_product(environ)
    elif path == "/shop":
        data: str = shop()
    elif path.startswith("/shop/product/added"):
        data: str = add_product_cart(environ, headers, cart)
    elif path == "/shoppingcart/show":
        data: str = shopping_cart(environ, cart)
    else:
        data: str = error404()

    data_in_bytes: bytes = data.encode("utf-8")

    headers.append(("Content-Length", str(len(data_in_bytes))))
    start_response("200 OK", headers)

    return iter([data_in_bytes])
