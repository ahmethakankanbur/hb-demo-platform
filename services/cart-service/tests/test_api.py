def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {
        "service": "cart-service",
        "status": "ok",
    }


def test_ready_endpoint(client):
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.get_json() == {
        "service": "cart-service",
        "status": "ready",
    }


def test_get_cart_returns_empty_cart_by_default(client):
    response = client.get("/api/v1/cart")

    assert response.status_code == 200
    assert response.get_json() == {
        "items": [],
        "item_count": 0,
        "total_quantity": 0,
    }


def test_add_cart_item_returns_updated_cart(client):
    response = client.post(
        "/api/v1/cart/items",
        json={"product_id": "sku-1001", "quantity": 2},
    )

    assert response.status_code == 200
    assert response.get_json() == {
        "items": [{"product_id": "sku-1001", "quantity": 2}],
        "item_count": 1,
        "total_quantity": 2,
    }


def test_add_cart_item_with_invalid_payload_returns_bad_request(client):
    response = client.post(
        "/api/v1/cart/items",
        json={"product_id": "sku-1001", "quantity": 0},
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "message": "quantity must be a positive integer",
    }


def test_delete_cart_item_removes_existing_item(client):
    client.post(
        "/api/v1/cart/items",
        json={"product_id": "sku-1001", "quantity": 2},
    )

    response = client.delete("/api/v1/cart/items/sku-1001")

    assert response.status_code == 200
    assert response.get_json() == {
        "items": [],
        "item_count": 0,
        "total_quantity": 0,
    }
