from typing import Optional
from uuid import uuid4
from urllib.parse import quote
from src.templates import render_template


class Product:

    def __init__(self, name: str, desc: str, price: float, uuid: Optional[str] = None) -> None:
        if uuid is not None:
            self.__uuid: str = uuid
        else:
            self.__uuid: str = str(uuid4())

        self.__name = name.strip()
        self.__desc = desc
        self.__price = price

    def __init_shop__(self, uuid: str, name: str, desc: str, price: float) -> None:

        self.__name = name.strip()
        self.__desc = desc
        self.__price = price

    @property
    def uuid(self) -> str:
        return self.__uuid

    @property
    def name(self) -> str:
        return self.__name

    @property
    def desc(self) -> str:
        return self.__desc

    @property
    def price(self) -> float:
        return self.__price

    def get_cookie(self) -> tuple[str, str]:
        product_name_enc: str = quote(self.__name)
        product_price_enc: str = self.__price
        product_desc_enc: str = quote(self.__desc)
        prod_uuid: str = self.__uuid

        return ("Set-Cookie",
                f"{prod_uuid}={1}"
                )


class ProductForm:
    def __init__(self, name: str, description: str, price: float) -> None:
        self.__uuid: str = str(uuid4())
        self.__name = name.strip()
        self.__desc = description
        self.__price = price

    def __get_productname_error(self) -> str:
        if not self.__name:
            return "Product name is required."
        return ""

    def __get_price_error(self) -> str:
        if not self.__price:
            return "Price field is required."
        if " " in self.__price:
            return "Price field cannot have spaces."
        if self.price_is_valid() is False:
            return "Price format is not valid."
        return ""

    def productname_is_valid(self) -> bool:
        if not self.__name:
            return False
        return True

    def price_is_valid(self) -> bool:
        if not str(self.__price).replace(",", ".").replace(".", "").isnumeric():
            return False
        price_check: list[str] = str(self.__price).replace(",", ".").split(".")
        if len(price_check) > 2:
            return False
        return True

    def get_context(self) -> dict[str, str]:
        return {
            "product_name": self.__name,
            "name_error": self.__get_productname_error(),
            "product_price": self.__price,
            "price_error": self.__get_price_error(),
            "styles": render_template("src/views/parts/style.html"),
            "nav": render_template("src/views/parts/nav.html"),
        }


class ShoppingCart:

    def __init__(self) -> None:
        self.__products: list[Product] = []

    def total_price(self) -> float:
        return sum([p.price for p in self.__products])

    @property
    def products(self) -> list[Product]:
        return self.__products

    def add_product(self, p: Product) -> None:
        self.__products.append(p)

    def remove_product(self, p: Product) -> None:
        self.__products = [
            product for product in self.__products
            if p != product
        ]

    def print_products(self) -> None:
        for product in self.__products:
            print(f"Product: {product.name}, Price: {product.price}")
