from __future__ import annotations

from flask import Blueprint, current_app, jsonify, request

from .clients import CartClient, CartServiceError, CatalogClient, CatalogServiceError

api_blueprint = Blueprint("api", __name__)


def build_proxy_response(response):
    if response.status_code == 204 or not response.content:
        return "", response.status_code

    return jsonify(response.json()), response.status_code


def get_catalog_client() -> CatalogClient:
    base_url = current_app.config.get("CATALOG_SERVICE_URL", "")
    timeout_seconds = current_app.config["REQUEST_TIMEOUT_SECONDS"]

    if not base_url:
        raise CatalogServiceError(
            "CATALOG_SERVICE_URL is not configured.",
            status_code=503,
        )

    return CatalogClient(base_url=base_url, timeout_seconds=timeout_seconds)


def get_cart_client() -> CartClient:
    base_url = current_app.config.get("CART_SERVICE_URL", "")
    timeout_seconds = current_app.config["REQUEST_TIMEOUT_SECONDS"]

    if not base_url:
        raise CartServiceError(
            "CART_SERVICE_URL is not configured.",
            status_code=503,
        )

    return CartClient(base_url=base_url, timeout_seconds=timeout_seconds)


@api_blueprint.get("/health")
def health() -> tuple[dict[str, str], int]:
    return {"status": "ok"}, 200


@api_blueprint.get("/ready")
def ready() -> tuple[dict[str, str], int]:
    try:
        get_catalog_client().check_ready()
        get_cart_client().check_ready()
    except (CatalogServiceError, CartServiceError) as exc:
        return jsonify({"status": "not_ready", "reason": str(exc)}), exc.status_code

    return {"status": "ready"}, 200


@api_blueprint.get("/api/v1/catalog/products")
def list_products():
    try:
        client = get_catalog_client()
        response = client.get_products(query_params=request.args.to_dict(flat=True))
    except CatalogServiceError as exc:
        return jsonify({"error": str(exc)}), exc.status_code

    return build_proxy_response(response)


@api_blueprint.get("/api/v1/catalog/products/<product_id>")
def get_product(product_id: str):
    try:
        client = get_catalog_client()
        response = client.get_product(product_id=product_id)
    except CatalogServiceError as exc:
        return jsonify({"error": str(exc)}), exc.status_code

    return build_proxy_response(response)


@api_blueprint.get("/api/v1/cart")
def get_cart():
    try:
        client = get_cart_client()
        response = client.get_cart(query_params=request.args.to_dict(flat=True))
    except CartServiceError as exc:
        return jsonify({"error": str(exc)}), exc.status_code

    return build_proxy_response(response)


@api_blueprint.post("/api/v1/cart/items")
def add_cart_item():
    try:
        client = get_cart_client()
        response = client.add_item(payload=request.get_json(silent=True))
    except CartServiceError as exc:
        return jsonify({"error": str(exc)}), exc.status_code

    return build_proxy_response(response)


@api_blueprint.delete("/api/v1/cart/items/<product_id>")
def remove_cart_item(product_id: str):
    try:
        client = get_cart_client()
        response = client.remove_item(product_id=product_id)
    except CartServiceError as exc:
        return jsonify({"error": str(exc)}), exc.status_code

    return build_proxy_response(response)
