from copy import deepcopy
from threading import Lock

from app.data.cart import build_cart_response


class InMemoryCartStore:
    def __init__(self) -> None:
        self._items: dict[str, dict[str, object]] = {}
        self._lock = Lock()

    def get_cart(self) -> dict[str, object]:
        with self._lock:
            items = [deepcopy(item) for item in self._items.values()]
        return build_cart_response(items)

    def upsert_item(self, product_id: str, quantity: int) -> dict[str, object]:
        with self._lock:
            self._items[product_id] = {
                "product_id": product_id,
                "quantity": quantity,
            }
            items = [deepcopy(item) for item in self._items.values()]
        return build_cart_response(items)

    def remove_item(self, product_id: str) -> bool:
        with self._lock:
            if product_id not in self._items:
                return False
            del self._items[product_id]
            return True
