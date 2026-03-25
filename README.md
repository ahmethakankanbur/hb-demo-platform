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
- [ ] Dockerfile ve `docker-compose.local.yml`
- [ ] Basit CI pipeline
- [ ] Kubernetes base manifestleri
- [ ] Overlay mantığı ile local/staging ayrımı
- [ ] Ingress, ConfigMap, Secret ve probe kullanımı

## Klasör Rehberi

- [`services`](/home/ahmet/code/hb-demo-platform/services/README.md): uygulama servisleri
- [`infra`](/home/ahmet/code/hb-demo-platform/infra/README.md): Docker, Compose, Kubernetes ve CI/CD yapıları
- [`docs`](/home/ahmet/code/hb-demo-platform/docs/README.md): mimari notlar ve ADR'ler
- [`scripts`](/home/ahmet/code/hb-demo-platform/scripts/README.md): geliştirme ve bootstrap scriptleri

## Not

Bu repo bilerek tam production karmaşıklığına çıkmaz. Ama dosya organizasyonu, isimlendirme ve operasyonel kavramlar açısından profesyonel bir temel sağlar.
