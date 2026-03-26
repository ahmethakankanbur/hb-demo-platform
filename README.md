# hb-demo-platform

Hepsiburada benzeri bir e-ticaret deneyimini modelleyen, öğrenme odaklı ve production-minded bir monorepo.

Bu repo şu konuları birlikte çalışmak için tasarlandı:

- Docker ve Docker Compose ile yerel geliştirme
- GitHub Actions ile temel CI akışı
- Kubernetes deployment mantığı
- Ingress, ConfigMap, Secret, liveness ve readiness probe kullanımı
- Monorepo düzeni, servis sınırları ve operasyonel düşünce biçimi

## Kısa Mimari Öneri

İlk aşamada yalın ama profesyonel görünen bir mikroservis yapısı önerilir:

- `frontend-web`: kullanıcı arayüzü
- `api-gateway`: istemcinin tek giriş noktası
- `catalog-service`: ürün listeleme ve ürün detayı
- `cart-service`: sepet işlemleri
- `postgres`: kalıcı veri
- `redis`: cache ve kısa süreli veri

İkinci aşamada eklenecek servisler:

- `order-service`: sipariş oluşturma ve durum takibi
- `identity-service`: kullanıcı ve basit kimlik doğrulama

Bu yapı öğrenme açısından yeterince gerçekçidir, fakat gereksiz erken karmaşıklık üretmez.

## Servisler ve Görevleri

| Servis | Sorumluluk | Faz |
| --- | --- | --- |
| `frontend-web` | Ürün listeleme, ürün detay, sepet akışı için web arayüzü | Faz 1 |
| `api-gateway` | Routing, basit auth kontrolü, response aggregation | Faz 1 |
| `catalog-service` | Ürün verisi, kategori, arama için API | Faz 1 |
| `cart-service` | Sepete ekleme, çıkarma, sepet görüntüleme | Faz 1 |
| `order-service` | Sipariş oluşturma, sipariş durumu | Faz 2 |
| `identity-service` | Kullanıcı profili, login/register için temel yapı | Faz 2 |
| `postgres` | Uygulama verisi | Faz 1 |
| `redis` | Cache, session, geçici state | Faz 1 |

## İlk Aşamada Nereden Başlamalı?

En doğru başlangıç seti:

1. `frontend-web`
2. `api-gateway`
3. `catalog-service`
4. `cart-service`
5. `postgres`
6. `redis`

Gerekçe: Bu altı bileşenle gerçek bir alışveriş akışı gösterilebilir. Aynı zamanda Docker Compose, container network, environment management, health check ve CI adımlarını öğretmek için yeterlidir.

## Monorepo Yapısı

```text
.
├── .github/
│   └── workflows/
├── docs/
│   ├── adr/
│   └── architecture.md
├── infra/
│   ├── compose/
│   ├── docker/
│   └── kubernetes/
├── scripts/
│   ├── bootstrap/
│   └── dev/
└── services/
    ├── api-gateway/
    ├── cart-service/
    ├── catalog-service/
    ├── frontend-web/
    ├── identity-service/
    └── order-service/
```

## Öğrenme Yol Haritası

- [x] Monorepo iskeleti
- [x] Mimari sınırların tanımlanması
- [ ] Faz 1 servislerinin ilk implementasyonu
- [x] Dockerfile ve `docker-compose.local.yml`
- [x] Basit CI pipeline
- [ ] Kubernetes base manifestleri
- [ ] Overlay mantığı ile local/staging ayrımı
- [ ] Ingress, ConfigMap, Secret ve probe kullanımı

## CI Pipeline

`.github/workflows/ci.yml` içindeki GitHub Actions workflow'u sadece `main` branch'i için çalışır:

- `push` ile `main` güncellendiğinde tetiklenir
- `pull_request` ile hedef branch `main` olduğunda tetiklenir
- `catalog-service` ve `api-gateway` için Python 3.12 kurar
- her iki servisin `requirements.txt` bağımlılıklarını yükler
- `compileall` ile temel Python syntax doğrulaması yapar
- iki servis için de Docker image build adımını doğrular

Bu akış şimdilik deployment yapmaz; amaç kod ve container seviyesinde erken doğrulama sağlamaktır.

## Klasör Rehberi

- [`services`](services/README.md): uygulama servisleri
- [`infra`](infra/README.md): Docker, Compose, Kubernetes ve CI/CD yapıları
- [`docs`](docs/README.md): mimari notlar ve ADR'ler
- [`scripts`](scripts/README.md): geliştirme ve bootstrap scriptleri

## Local Compose ile Başlatma

Yerel olarak ilk çalışan akış şu iki servisten oluşur:

- `catalog-service`
- `api-gateway`

Compose dosyası:

- her iki servisi source üzerinden build eder
- port eşlemesi kurar: `8080:8080` ve `8081:8081`
- ortak network üstünde servis keşfi sağlar
- gateway içinde `CATALOG_SERVICE_URL=http://catalog-service:8081` ayarını kullanır

Başlatma:

```bash
docker compose -f infra/compose/docker-compose.local.yml up --build
```

Arka planda çalıştırma:

```bash
docker compose -f infra/compose/docker-compose.local.yml up --build -d
```

Kontrol:

```bash
curl http://localhost:8081/health
curl http://localhost:8080/health
curl http://localhost:8080/api/v1/catalog/products
```

## Not

Bu repo bilerek tam production karmaşıklığına çıkmaz. Ama dosya organizasyonu, isimlendirme ve operasyonel kavramlar açısından profesyonel bir temel sağlar.
