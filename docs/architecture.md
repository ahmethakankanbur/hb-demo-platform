# Mimari Özeti

## Amaç

Bu platform, Hepsiburada benzeri bir e-ticaret akışını küçük ama gerçekçi servis sınırlarıyla modellemek için tasarlanır.

## Yüksek Seviye Akış

1. Kullanıcı `frontend-web` üzerinden işlem yapar.
2. İstekler `api-gateway` üzerinden ilgili servislere yönlenir.
3. Ürün verisi `catalog-service` tarafından sunulur.
4. Sepet işlemleri `cart-service` tarafından yönetilir.
5. Sonraki fazda sipariş ve kimlik yönetimi ayrı servislere taşınır.

## Neden Bu Tasarım?

- Öğrenmesi kolaydır.
- Container ve orchestration kavramlarını göstermek için yeterlidir.
- Portföyde profesyonel görünür.
- Erken aşamada event bus, service mesh veya observability stack gibi ağır bağımlılıklar eklemez.

## Veri ve Altyapı

- `postgres`: ilişkisel veri saklama
- `redis`: cache ve transient state

## Kubernetes Öğrenme Alanları

- `Deployment`: uygulama rollout mantığı
- `Service`: pod erişimi
- `Ingress`: dış trafik girişi
- `ConfigMap`: non-secret config
- `Secret`: hassas değişkenler
- `Probe`: uygulama sağlığı

## Faz Planı

### Faz 1

Çalışan demo akışı:

- frontend
- gateway
- catalog
- cart
- postgres
- redis

### Faz 2

Alanı genişletme:

- order
- identity
- staging overlay
- basit CI/CD geliştirmeleri
