# catalog-service

`catalog-service`, demo platform için ürün katalog verisini sunan sade bir Flask servisidir.

Servis şu uçları sağlar:

- `GET /health`
- `GET /ready`
- `GET /api/v1/products`
- `GET /api/v1/products/<product_id>`

Uygulama application factory pattern ile kurulmuştur ve production çalıştırma için `gunicorn` kullanır.

## Dizin Yapısı

```text
catalog-service/
├── app/
│   ├── api/
│   ├── data/
│   ├── __init__.py
│   └── config.py
├── Dockerfile
├── requirements.txt
└── wsgi.py
```

## Lokal Çalıştırma

Python 3.12+ önerilir.

Bağımlılıkları yükle:

```bash
pip install -r requirements.txt
```

Testleri çalıştır:

```bash
pytest
```

Servisi `gunicorn` ile başlat:

```bash
gunicorn --bind 0.0.0.0:8081 --workers 2 --threads 4 wsgi:app
```

Servis ayağa kalktıktan sonra taban adres:

```text
http://localhost:8081
```

## Docker ile Çalıştırma

Image oluştur:

```bash
docker build -t hb-demo/catalog-service:local .
```

Container çalıştır:

```bash
docker run --rm -p 8081:8081 hb-demo/catalog-service:local
```

## API Davranışı

### Health

Kubernetes liveness probe beklentisiyle uyumlu uç:

```http
GET /health
```

Örnek yanıt:

```json
{
  "service": "catalog-service",
  "status": "ok"
}
```

### Readiness

Kubernetes readiness probe beklentisiyle uyumlu uç:

```http
GET /ready
```

Örnek yanıt:

```json
{
  "service": "catalog-service",
  "status": "ready"
}
```

### Product List

Seed data ile çalışan ürün listesi:

```http
GET /api/v1/products
```

### Product Detail

Belirli bir ürün kaydını döner:

```http
GET /api/v1/products/<product_id>
```

Bulunamayan ürün için `404` döner.

## curl Örnekleri

Health kontrolü:

```bash
curl http://localhost:8081/health
```

Readiness kontrolü:

```bash
curl http://localhost:8081/ready
```

Tüm ürünleri listele:

```bash
curl http://localhost:8081/api/v1/products
```

Tek ürün getir:

```bash
curl http://localhost:8081/api/v1/products/sku-1001
```

Olmayan ürün örneği:

```bash
curl http://localhost:8081/api/v1/products/unknown-product
```

## Notlar

- Container portu `8081` olarak ayarlanmıştır.
- `infra/kubernetes/base/catalog-service-deployment.yaml` içindeki `/health` ve `/ready` probe path'leri ile uyumludur.
- Veri kaynağı şu an seed data'dır; daha sonra repository veya veritabanı katmanına genişletilebilir.
