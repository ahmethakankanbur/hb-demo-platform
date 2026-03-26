# infra

Bu klasör operasyonel katmanı taşır.

## Alt Klasörler

- `docker/`: ortak container kalıpları ve örnek Docker yapılandırmaları
- `compose/`: yerel geliştirme için Docker Compose dosyaları
- `kubernetes/base/`: ortamdan bağımsız temel manifestler
- `kubernetes/overlays/`: local ve staging gibi ortam bazlı özelleştirmeler

## Öğrenme Hedefleri

- container lifecycle
- servis keşfi ve ağ iletişimi
- config ayrıştırma
- health probe mantığı
- deployment ve rollout davranışı

## CI

Repository içindeki GitHub Actions workflow'u `.github/workflows/ci.yml` dosyasında yer alır. Bu pipeline:

- sadece `main` için `push` ve `pull_request` eventlerinde çalışır
- `catalog-service` ve `api-gateway` bağımlılıklarını kurar
- Python syntax doğrulaması yapar
- her iki servisin Docker image build adımını kontrol eder

Bu aşamada deployment yoktur; workflow yalnızca CI doğrulaması sağlar.

## Local Compose

`infra/compose/docker-compose.local.yml` yerel geliştirme için sade bir üç servis akışı sağlar:

- `catalog-service` kendi container'ında `8081` portunda çalışır
- `cart-service` kendi container'ında `8082` portunda çalışır
- `api-gateway` `8080` portunda çalışır
- üç servis aynı Docker network içindedir
- `api-gateway`, `catalog-service` servisine `http://catalog-service:8081` adresiyle erişir
- `api-gateway`, `cart-service` servisine `http://cart-service:8082` adresiyle erişir

Çalıştırma:

```bash
docker compose -f infra/compose/docker-compose.local.yml up --build
```

Arka planda çalıştırma:

```bash
docker compose -f infra/compose/docker-compose.local.yml up --build -d
```

Durdurma:

```bash
docker compose -f infra/compose/docker-compose.local.yml down
```

Doğrulama:

```bash
curl http://localhost:8081/health
curl http://localhost:8082/health
curl http://localhost:8080/health
curl http://localhost:8080/api/v1/catalog/products
```
