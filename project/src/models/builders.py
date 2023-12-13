from http.cookies import SimpleCookie
from urllib.parse import unquote

from src.models.shopping_cart import Product, ShoppingCart, ProductForm
from src.templates import render_template


def build_shopping_cart():
    pass


def build_product(form: dict[str, str]) -> Product:
    return Product(
        name=form["name"] if "name" in form else "",
        price=float(form["price"].replace(
            ",", ".")) if "price" in form else 0.0,
        desc=form["description"] if "description" in form else ""
    )
