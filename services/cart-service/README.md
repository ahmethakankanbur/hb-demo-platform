# cart-service

`cart-service`, demo platform için sepet işlemlerini yöneten sade ama production-minded bir Flask servisidir.

İlk sürümde veri katmanı olarak in-memory state kullanır. Uygulama application factory pattern ile kurulmuştur ve runtime için Flask built-in server yerine `gunicorn` kullanır.

## Dizin Yapısı

```text
cart-service/
├── app/
│   ├── api/
│   ├── data/
│   ├── state/
│   ├── __init__.py
│   └── config.py
├── Dockerfile
├── requirements.txt
└── wsgi.py
```

## Endpointler

- `GET /health`
- `GET /ready`
- `GET /api/v1/cart`
- `POST /api/v1/cart/items`
- `DELETE /api/v1/cart/items/<product_id>`

## Lokal Çalıştırma

Python 3.12+ önerilir.

Bağımlılıkları yükle:

```bash
pip install -r requirements.txt
```

Servisi `gunicorn` ile başlat:

```bash
gunicorn --bind 0.0.0.0:8082 --workers 1 --threads 4 wsgi:app
```

Servis ayağa kalktıktan sonra taban adres:

```text
http://localhost:8082
```

## Docker ile Çalıştırma

Image oluştur:

```bash
docker build -t hb-demo/cart-service:local .
```

Container çalıştır:

```bash
docker run --rm -p 8082:8082 hb-demo/cart-service:local
```

## API Davranışı

### Health

```http
GET /health
```

Örnek yanıt:

```json
{
  "service": "cart-service",
  "status": "ok"
}
```

### Readiness

```http
GET /ready
```

Örnek yanıt:

```json
{
  "service": "cart-service",
  "status": "ready"
}
```

### Cart Getir

```http
GET /api/v1/cart
```

Örnek yanıt:

```json
{
  "item_count": 2,
  "items": [
    {
      "product_id": "sku-1001",
      "quantity": 2
    },
    {
      "product_id": "sku-2001",
      "quantity": 1
    }
  ],
  "total_quantity": 3
}
```

### Sepete Ürün Ekle veya Güncelle

```http
POST /api/v1/cart/items
Content-Type: application/json
```

İstek gövdesi:

```json
{
  "product_id": "sku-1001",
  "quantity": 2
}
```

Kurallar:

- `product_id` boş olmayan string olmalıdır.
- `quantity` pozitif tam sayı olmalıdır.
- Ürün sepette varsa quantity değeri güncellenir.
- Ürün yoksa yeni item eklenir.

Geçersiz istek için `400` döner.

### Sepetten Ürün Sil

```http
DELETE /api/v1/cart/items/<product_id>
```

Ürün sepette yoksa `404` döner.

## curl Örnekleri

Health kontrolü:

```bash
curl http://localhost:8082/health
```

Readiness kontrolü:

```bash
curl http://localhost:8082/ready
```

Sepeti getir:

```bash
curl http://localhost:8082/api/v1/cart
```

Sepete ürün ekle:

```bash
curl -X POST http://localhost:8082/api/v1/cart/items \
  -H "Content-Type: application/json" \
  -d '{"product_id":"sku-1001","quantity":2}'
```

Sepetteki ürün quantity güncelle:

```bash
curl -X POST http://localhost:8082/api/v1/cart/items \
  -H "Content-Type: application/json" \
  -d '{"product_id":"sku-1001","quantity":5}'
```

Sepetten ürün sil:

```bash
curl -X DELETE http://localhost:8082/api/v1/cart/items/sku-1001
```

Geçersiz quantity örneği:

```bash
curl -X POST http://localhost:8082/api/v1/cart/items \
  -H "Content-Type: application/json" \
  -d '{"product_id":"sku-1001","quantity":0}'
```

## Notlar

- Container portu `8082` olarak ayarlanmıştır.
- In-memory state process bazlıdır; container restart olduğunda veri sıfırlanır.
- Bu nedenle `gunicorn` tek worker ile çalıştırılır; aksi halde her worker kendi ayrı sepet state'ini tutar.
- Kalıcı ve paylaşımlı state için sonraki adımda Redis veya veritabanı katmanı eklenmelidir.
