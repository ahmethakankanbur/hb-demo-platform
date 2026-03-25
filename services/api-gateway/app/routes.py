from __future__ import annotations

from flask import Blueprint, current_app, jsonify, request

from .clients import CatalogClient, CatalogServiceError

api_blueprint = Blueprint("api", __name__)


def get_catalog_client() -> CatalogClient:
    base_url = current_app.config.get("CATALOG_SERVICE_URL", "")
    timeout_seconds = current_app.config["REQUEST_TIMEOUT_SECONDS"]

    if not base_url:
        raise CatalogServiceError(
            "CATALOG_SERVICE_URL is not configured.",
            status_code=503,
        )

    return CatalogClient(base_url=base_url, timeout_seconds=timeout_seconds)


@api_blueprint.get("/health")
def health() -> tuple[dict[str, str], int]:
    return {"status": "ok"}, 200


@api_blueprint.get("/ready")
def ready() -> tuple[dict[str, str], int]:
    try:
        client = get_catalog_client()
        client.check_ready()
    except CatalogServiceError as exc:
        return jsonify({"status": "not_ready", "reason": str(exc)}), exc.status_code

    return {"status": "ready"}, 200


@api_blueprint.get("/api/v1/catalog/products")
def list_products():
    try:
        client = get_catalog_client()
        response = client.get_products(query_params=request.args.to_dict(flat=True))
    except CatalogServiceError as exc:
        return jsonify({"error": str(exc)}), exc.status_code

    return jsonify(response.json()), response.status_code


@api_blueprint.get("/api/v1/catalog/products/<product_id>")
def get_product(product_id: str):
    try:
        client = get_catalog_client()
        response = client.get_product(product_id=product_id)
    except CatalogServiceError as exc:
        return jsonify({"error": str(exc)}), exc.status_code

    return jsonify(response.json()), response.status_code
