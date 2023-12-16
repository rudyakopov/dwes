from http.cookies import SimpleCookie
from urllib.parse import parse_qs
from multipart import parse_form_data

from src.models.builders import build_product
from src.models.shopping_cart import Product, ShoppingCart, ProductForm
from src.templates import render_template
from src.db.database import insert, get_product, get_products

cart: ShoppingCart = ShoppingCart()

context: dict[str, str] = {
    "product_name": "",
    "name_error": "",
    "price_error": "",
    "product_price": "",
    "products": "",
    "empty_shop": "",
    "empty_cart": "",
    "total": "",
    "t_name": "",
    "t_price": "",
    "t_total": "",
    "nav": render_template("src/views/parts/nav.html"),
    "styles": render_template("src/views/parts/style.html")
}


def home() -> str:
    return render_template("src/views/index.html", context)


def add_product(environ: dict[str, list[str]]) -> str:

    method: str = environ.get("REQUEST_METHOD", "").upper()
    if method != "POST":
        return render_template(
            "src/views/form_add_product.html", context)

    form, _ = parse_form_data(environ)
    product_form: ProductForm = ProductForm(**form)

    if product_form.price_is_valid() and product_form.productname_is_valid():
        product: Product = build_product(form)
        insert(product)

        return render_template("src/views/product_added.html", {
            "nav": render_template("src/views/parts/nav.html"),
            "styles": render_template("src/views/parts/style.html"),
            "product_name": product.name,
            "product_price": product.price,
        })
    else:
        return render_template(
            "src/views/form_add_product.html",
            product_form.get_context()
        )


def shop() -> str:

    if len(get_products()) != 0:
        products_html: str = ""
        for product in get_products():
            products_html += f"<tr><td>{product.name}</td>"
            products_html += f"<td>{product.desc}</td>"
            products_html += f"<td>{product.price}</td>"
            products_html += f"<td><a href='/shop/product/added?uuid={product.uuid}'>Añadir al carrito!</td></tr>"

    elif len(get_products()) == 0:
        products_html: str = ""
        context["empty_shop"] = "<h3>Actualmente no tenemos stock. Hasta pronto!<h3>"

        return render_template("src/views/shop.html", context)

    context["products"] = products_html

    return render_template("src/views/shop.html", context)


def add_product_cart(environ: dict[str, list[str]], headers: list[tuple[str, str]], cart: ShoppingCart) -> str:

    cookies: SimpleCookie = SimpleCookie()
    cookies.load(environ["HTTP_COOKIE"])

    qs_dict: dict[str, str] = parse_qs(environ["QUERY_STRING"])
    qs_uuid: str = qs_dict["uuid"][0]

    if get_product(qs_uuid).uuid in [product.uuid for product in cart.products]:
        units: int = int(cookies[qs_uuid].value) + 1
        new_cookie: tuple = ("Set-Cookie",
                             f"{get_product(qs_uuid).uuid}={units}"
                             )
        headers.append(new_cookie)
        product: Product = get_product(qs_uuid)
        cart.add_product(product)

    else:
        headers.append(get_product(qs_uuid).get_cookie())
        cart.add_product(get_product(qs_uuid))
        context["product_name"] = get_product(qs_uuid).name

    return render_template("src/views/msg_prod_added.html", context)


def shopping_cart(environ: dict[str, list[str]], cart: ShoppingCart) -> str:
    pr_cart_html: str = ""
    if cart.products:
        for x in cart.products:
            pr_cart_html += f"<tr><td>{x.name}</td>"
            pr_cart_html += f"<td>{x.price}</td><tr/>"
        context["products"] = pr_cart_html
        context["t_name"] = "Nombre"
        context["t_price"] = "Precio"
        context["t_total"] = "TOTAL"
        context["total"] = f"<td style='font-weight: bold;'>{cart.total_price()}</td>"
    else:
        context["products"] = "<h3>La cesta está vacía :(<h3>"

    return render_template("src/views/myCart.html", context)


def error404():
    return render_template("src/views/404.html", context)
