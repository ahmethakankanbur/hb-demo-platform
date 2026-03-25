# api-gateway

İstemciler için tek giriş noktası olan ilk gerçek gateway servisi.

Bu servis:

- Flask application factory pattern kullanır
- `catalog-service` isteklerini proxy eder
- health ve readiness endpointleri sunar
- Flask built-in server yerine Gunicorn ile çalışır

## Endpointler

- `GET /health`
- `GET /ready`
- `GET /api/v1/catalog/products`
- `GET /api/v1/catalog/products/<product_id>`

## Environment Variables

- `CATALOG_SERVICE_URL`: catalog-service base URL'i
- `REQUEST_TIMEOUT_SECONDS`: upstream request timeout değeri

Örnek:

```bash
export CATALOG_SERVICE_URL=http://catalog-service:8081
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

## Readiness Davranışı

- `CATALOG_SERVICE_URL` tanımlı değilse `503` döner
- gateway `catalog-service` içindeki `/health` endpointine erişemiyorsa `503` veya upstream hata kodu döner
- upstream hazırsa `200` ve `{"status":"ready"}` döner
