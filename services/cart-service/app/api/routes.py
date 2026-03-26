from flask import current_app, jsonify, request

from app.api import api_bp
from app.config import Config
from app.state.cart_store import InMemoryCartStore

API_PREFIX = Config.API_PREFIX


def get_cart_store() -> InMemoryCartStore:
    return current_app.extensions["cart_store"]


def validate_add_item_payload(payload: object) -> tuple[dict[str, object] | None, tuple[object, int] | None]:
    if not isinstance(payload, dict):
        return None, (jsonify({"message": "Request body must be a JSON object"}), 400)

    product_id = payload.get("product_id")
    quantity = payload.get("quantity")

    if not isinstance(product_id, str) or not product_id.strip():
        return None, (jsonify({"message": "product_id must be a non-empty string"}), 400)

    if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
        return None, (jsonify({"message": "quantity must be a positive integer"}), 400)

    return {"product_id": product_id.strip(), "quantity": quantity}, None


@api_bp.get("/health")
def health() -> tuple[dict[str, str], int]:
    return (
        {
            "status": "ok",
            "service": current_app.config["SERVICE_NAME"],
        },
        200,
    )


@api_bp.get("/ready")
def ready() -> tuple[dict[str, str], int]:
    return (
        {
            "status": "ready",
            "service": current_app.config["SERVICE_NAME"],
        },
        200,
    )


@api_bp.get(f"{API_PREFIX}/cart")
def get_cart() -> tuple[object, int]:
    cart = get_cart_store().get_cart()
    return jsonify(cart), 200


@api_bp.post(f"{API_PREFIX}/cart/items")
def add_cart_item() -> tuple[object, int]:
    payload, error_response = validate_add_item_payload(request.get_json(silent=True))
    if error_response is not None:
        return error_response

    assert payload is not None
    cart = get_cart_store().upsert_item(
        product_id=payload["product_id"],
        quantity=payload["quantity"],
    )
    return jsonify(cart), 200


@api_bp.delete(f"{API_PREFIX}/cart/items/<product_id>")
def delete_cart_item(product_id: str) -> tuple[object, int]:
    removed = get_cart_store().remove_item(product_id)
    if not removed:
        return jsonify({"message": "Product not found in cart", "product_id": product_id}), 404

    cart = get_cart_store().get_cart()
    return jsonify(cart), 200
