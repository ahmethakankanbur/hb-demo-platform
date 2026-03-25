from flask import current_app, jsonify

from app.api import api_bp
from app.data.products import get_product_by_id, list_products


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


@api_bp.get("/api/v1/products")
def products() -> tuple[object, int]:
    items = list_products()
    return jsonify({"items": items, "count": len(items)}), 200


@api_bp.get("/api/v1/products/<product_id>")
def product_detail(product_id: str) -> tuple[object, int]:
    product = get_product_by_id(product_id)
    if product is None:
        return jsonify({"message": "Product not found", "product_id": product_id}), 404
    return jsonify(product), 200
