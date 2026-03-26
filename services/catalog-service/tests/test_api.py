def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {
        "service": "catalog-service",
        "status": "ok",
    }


def test_ready_endpoint(client):
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.get_json() == {
        "service": "catalog-service",
        "status": "ready",
    }


def test_get_products_returns_seed_data(client):
    response = client.get("/api/v1/products")

    payload = response.get_json()

    assert response.status_code == 200
    assert payload["count"] == 3
    assert len(payload["items"]) == 3
    assert payload["items"][0]["id"] == "sku-1001"


def test_get_product_by_valid_id_returns_product(client):
    response = client.get("/api/v1/products/sku-1002")

    assert response.status_code == 200
    assert response.get_json() == {
        "id": "sku-1002",
        "name": "Cotton Throw Blanket",
        "category": "home",
        "price": 699.0,
        "currency": "TRY",
        "stock_status": "limited",
    }


def test_get_product_by_invalid_id_returns_not_found(client):
    response = client.get("/api/v1/products/unknown-product")

    assert response.status_code == 404
    assert response.get_json() == {
        "message": "Product not found",
        "product_id": "unknown-product",
    }
