# api-gateway

İstemciler için tek giriş noktası olan ilk gerçek gateway servisi.

Bu servis:

- Flask application factory pattern kullanır
- `catalog-service` ve `cart-service` isteklerini proxy eder
- health ve readiness endpointleri sunar
- Flask built-in server yerine Gunicorn ile çalışır

## Endpointler

- `GET /health`
- `GET /ready`
- `GET /api/v1/catalog/products`
- `GET /api/v1/catalog/products/<product_id>`
- `GET /api/v1/cart`
- `POST /api/v1/cart/items`
- `DELETE /api/v1/cart/items/<product_id>`

## Environment Variables

- `CATALOG_SERVICE_URL`: catalog-service base URL'i
- `CART_SERVICE_URL`: cart-service base URL'i
- `REQUEST_TIMEOUT_SECONDS`: upstream request timeout değeri

Örnek:

```bash
export CATALOG_SERVICE_URL=http://catalog-service:8081
export CART_SERVICE_URL=http://cart-service:8082
export REQUEST_TIMEOUT_SECONDS=5
```

## Lokal Çalıştırma

1. Bağımlılıkları kur:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Environment variable'ları ayarla:

```bash
export CATALOG_SERVICE_URL=http://localhost:8081
export CART_SERVICE_URL=http://localhost:8082
export REQUEST_TIMEOUT_SECONDS=5
```

3. Servisi başlat:

```bash
gunicorn --bind 0.0.0.0:8080 --workers 2 --threads 4 --timeout 30 wsgi:app
```

## Docker ile Çalıştırma

Image build:

```bash
docker build -t api-gateway .
```

Container run:

```bash
docker run --rm -p 8080:8080 \
  -e CATALOG_SERVICE_URL=http://host.docker.internal:8081 \
  -e CART_SERVICE_URL=http://host.docker.internal:8082 \
  -e REQUEST_TIMEOUT_SECONDS=5 \
  api-gateway
```

## Curl Örnekleri

Health:

```bash
curl -i http://localhost:8080/health
```

Readiness:

```bash
curl -i http://localhost:8080/ready
```

Ürün listesi:

```bash
curl -i http://localhost:8080/api/v1/catalog/products
```

Tek ürün:

```bash
curl -i http://localhost:8080/api/v1/catalog/products/123
```

Query param ile ürün listesi:

```bash
curl -i "http://localhost:8080/api/v1/catalog/products?limit=10&category=electronics"
```

Sepet:

```bash
curl -i "http://localhost:8080/api/v1/cart?user_id=u1"
```

Sepete ürün ekleme:

```bash
curl -i -X POST http://localhost:8080/api/v1/cart/items \
  -H "Content-Type: application/json" \
  -d '{"user_id":"u1","product_id":"123","quantity":1}'
```

Sepetten ürün silme:

```bash
curl -i -X DELETE http://localhost:8080/api/v1/cart/items/123
```

## Readiness Davranışı

- `CATALOG_SERVICE_URL` tanımlı değilse `503` döner
- `CART_SERVICE_URL` tanımlı değilse `503` döner
- gateway upstream servislerin `/health` endpointlerine erişemiyorsa `503` veya upstream hata kodu döner
- upstream hazırsa `200` ve `{"status":"ready"}` döner
