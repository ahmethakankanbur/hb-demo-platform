from copy import deepcopy

PRODUCTS = [
    {
        "id": "sku-1001",
        "name": "Anatolian Coffee Mug",
        "category": "kitchen",
        "price": 249.90,
        "currency": "TRY",
        "stock_status": "in_stock",
    },
    {
        "id": "sku-1002",
        "name": "Cotton Throw Blanket",
        "category": "home",
        "price": 699.00,
        "currency": "TRY",
        "stock_status": "limited",
    },
    {
        "id": "sku-1003",
        "name": "Wireless Desk Lamp",
        "category": "electronics",
        "price": 1199.50,
        "currency": "TRY",
        "stock_status": "in_stock",
    },
]


def list_products() -> list[dict]:
    return deepcopy(PRODUCTS)


def get_product_by_id(product_id: str) -> dict | None:
    for product in PRODUCTS:
        if product["id"] == product_id:
            return deepcopy(product)
    return None
