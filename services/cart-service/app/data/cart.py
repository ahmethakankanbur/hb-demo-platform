def build_cart_response(items: list[dict[str, object]]) -> dict[str, object]:
    total_quantity = sum(item["quantity"] for item in items)
    return {
        "items": items,
        "item_count": len(items),
        "total_quantity": total_quantity,
    }
