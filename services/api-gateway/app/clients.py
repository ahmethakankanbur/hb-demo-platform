from __future__ import annotations

from urllib.parse import urljoin

import requests


class CatalogServiceError(Exception):
    def __init__(self, message: str, status_code: int = 502) -> None:
        super().__init__(message)
        self.status_code = status_code


class CatalogClient:
    def __init__(self, base_url: str, timeout_seconds: float) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def check_ready(self) -> None:
        self._get("/health")

    def get_products(self, query_params: dict[str, str]) -> requests.Response:
        return self._get("/api/v1/products", params=query_params)

    def get_product(self, product_id: str) -> requests.Response:
        return self._get(f"/api/v1/products/{product_id}")

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
            raise CatalogServiceError(
                f"Catalog service returned HTTP {status_code}.",
                status_code=status_code,
            ) from exc
        except requests.exceptions.RequestException as exc:
            raise CatalogServiceError("Catalog service is unavailable.", status_code=502) from exc

        return response
