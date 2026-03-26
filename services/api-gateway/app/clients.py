from __future__ import annotations

from urllib.parse import urljoin

import requests


class UpstreamServiceError(Exception):
    def __init__(self, message: str, status_code: int = 502) -> None:
        super().__init__(message)
        self.status_code = status_code


class BaseServiceClient:
    service_name = "Upstream service"
    error_cls = UpstreamServiceError

    def __init__(self, base_url: str, timeout_seconds: float) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def check_ready(self) -> None:
        self._get("/health")

    def _get(
        self,
        path: str,
        params: dict[str, str] | None = None,
    ) -> requests.Response:
        url = urljoin(f"{self.base_url}/", path.lstrip("/"))

        try:
            response = requests.get(url, params=params, timeout=self.timeout_seconds)
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            status_code = exc.response.status_code if exc.response is not None else 502
            raise self.error_cls(
                f"{self.service_name} returned HTTP {status_code}.",
                status_code=status_code,
            ) from exc
        except requests.exceptions.RequestException as exc:
            raise self.error_cls(f"{self.service_name} is unavailable.", status_code=502) from exc

        return response

    def _post(
        self,
        path: str,
        json_body: dict | list | None = None,
    ) -> requests.Response:
        url = urljoin(f"{self.base_url}/", path.lstrip("/"))

        try:
            response = requests.post(url, json=json_body, timeout=self.timeout_seconds)
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            status_code = exc.response.status_code if exc.response is not None else 502
            raise self.error_cls(
                f"{self.service_name} returned HTTP {status_code}.",
                status_code=status_code,
            ) from exc
        except requests.exceptions.RequestException as exc:
            raise self.error_cls(f"{self.service_name} is unavailable.", status_code=502) from exc

        return response

    def _delete(self, path: str) -> requests.Response:
        url = urljoin(f"{self.base_url}/", path.lstrip("/"))

        try:
            response = requests.delete(url, timeout=self.timeout_seconds)
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            status_code = exc.response.status_code if exc.response is not None else 502
            raise self.error_cls(
                f"{self.service_name} returned HTTP {status_code}.",
                status_code=status_code,
            ) from exc
        except requests.exceptions.RequestException as exc:
            raise self.error_cls(f"{self.service_name} is unavailable.", status_code=502) from exc

        return response


class CatalogServiceError(UpstreamServiceError):
    pass


class CatalogClient(BaseServiceClient):
    service_name = "Catalog service"
    error_cls = CatalogServiceError

    def get_products(self, query_params: dict[str, str]) -> requests.Response:
        return self._get("/api/v1/products", params=query_params)

    def get_product(self, product_id: str) -> requests.Response:
        return self._get(f"/api/v1/products/{product_id}")


class CartServiceError(UpstreamServiceError):
    pass


class CartClient(BaseServiceClient):
    service_name = "Cart service"
    error_cls = CartServiceError

    def get_cart(self, query_params: dict[str, str]) -> requests.Response:
        return self._get("/api/v1/cart", params=query_params)

    def add_item(self, payload: dict | list | None) -> requests.Response:
        return self._post("/api/v1/cart/items", json_body=payload)

    def remove_item(self, product_id: str) -> requests.Response:
        return self._delete(f"/api/v1/cart/items/{product_id}")
