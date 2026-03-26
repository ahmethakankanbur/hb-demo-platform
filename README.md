# hb-demo-platform

Hepsiburada benzeri bir e-ticaret deneyimini modelleyen, öğrenme odakli ve production-minded bir monorepo. Repo; servis sinirlari, local development, temel CI akisi ve Kubernetes'e hazir altyapi dusuncesi uzerine kuruludur.

[![Service CI Checks](https://github.com/ahmethakankanbur/hb-demo-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/ahmethakankanbur/hb-demo-platform/actions/workflows/ci.yml)

## Tech Stack

- Python 3.12
- Flask tabanli HTTP servisleri
- Docker ve Docker Compose
- GitHub Actions
- Kubernetes ve Kustomize tabanli manifest yapisi

## Current Services

Su an repo icinde tanimli veya planlanmis servisler:

| Service | Responsibility | Status |
| --- | --- | --- |
| `frontend-web` | Web arayuzu | Planlanmis |
| `api-gateway` | Routing, basit auth kontrolu, response aggregation | Mevcut |
| `catalog-service` | Urun listeleme, urun detayi ve katalog API'si | Mevcut |
| `cart-service` | Sepet islemleri | Iskelet asamasinda |
| `order-service` | Siparis olusturma ve durum takibi | Planlanmis |
| `identity-service` | Kullanici ve temel kimlik dogrulama yapisi | Planlanmis |
| `postgres` | Kalici veri katmani | Mimari hedef |
| `redis` | Cache ve kisa sureli veri | Mimari hedef |

Bugun itibariyla local compose akisi `catalog-service`, `cart-service` ve `api-gateway` uzerinden calisir. Bu uc servis, repo icindeki ilk gercek servis etkilesimini ve local entegrasyon akisini temsil eder.

## Architecture Snapshot

Ilk asamada yalniz ama profesyonel gorunen bir mikroservis yapisi hedeflenir:

- `frontend-web`
- `api-gateway`
- `catalog-service`
- `cart-service`
- `postgres`
- `redis`

Ikinci asamada eklenmesi planlanan servisler:

- `order-service`
- `identity-service`

Bu yapi, gereksiz erken karmasiklik uretmeden servis sinirlari, container tabanli gelistirme ve operasyonel dusunce bicimi uzerinde calismak icin yeterli bir temel saglar.

## Repository Layout

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

Ek klasor rehberi:

- [`services`](services/README.md): uygulama servisleri
- [`infra`](infra/README.md): Docker, Compose, Kubernetes ve CI/CD yapilari
- [`docs`](docs/README.md): mimari notlar ve ADR'ler
- [`scripts`](scripts/README.md): gelistirme ve bootstrap scriptleri

## Quick Start

Yerelde en hizli calisan senaryo uc servisten olusur:

- `catalog-service` on `localhost:8081`
- `cart-service` on `localhost:8082`
- `api-gateway` on `localhost:8080`

Calistir:

```bash
docker compose -f infra/compose/docker-compose.local.yml up --build
```

Arka planda calistir:

```bash
docker compose -f infra/compose/docker-compose.local.yml up --build -d
```

Saglik ve ornek istek kontrolu:

```bash
curl http://localhost:8081/health
curl http://localhost:8082/health
curl http://localhost:8080/health
curl http://localhost:8080/api/v1/catalog/products
```

Local compose yapisi:

- uc servisi source uzerinden build eder
- `8080:8080`, `8081:8081` ve `8082:8082` port eslemesini kullanir
- ortak Docker network uzerinde servis kesfi saglar
- gateway icinde `CATALOG_SERVICE_URL=http://catalog-service:8081` ayari ile katalog servisine erisir
- gateway icinde `CART_SERVICE_URL=http://cart-service:8082` ayari ile cart servisine erisir

## Request Flow

Bugun calisan temel akis su sekildedir: client istegi once `api-gateway`'e gelir, gateway ilgili endpoint'e gore istegi `catalog-service` veya `cart-service` servisine iletir ve yaniti geri doner.

```text
Client
  -> api-gateway
       -> catalog-service
       -> cart-service
```

Local makinadan erisim icin `localhost:8080`, `localhost:8081` ve `localhost:8082` kullanilir. Container'lar kendi aralarinda ise Docker network uzerinden `catalog-service:8081` ve `cart-service:8082` gibi service-name ile haberlesir; `localhost` burada container'in kendi icini ifade eder.

## CI Pipeline

`.github/workflows/ci.yml` altindaki GitHub Actions workflow'u sadece `main` branch'i icin calisir:

- `push` ile `main` guncellendiginde tetiklenir
- hedefi `main` olan `pull_request` olaylarinda tetiklenir
- `catalog-service`, `api-gateway` ve `cart-service` icin Python 3.12 kurar
- ilgili `requirements.txt` bagimliliklarini yukler
- `compileall` ile temel Python syntax dogrulamasi yapar
- uc servis icin Docker image build adimini validate eder

Bu akis su an deployment yapmaz; amac kod ve container seviyesinde erken dogrulamadir.

## Project Status

- Monorepo iskeleti olusturuldu
- Servis sinirlari ve klasor organizasyonu tanimlandi
- `catalog-service`, `cart-service` ve `api-gateway` icin local compose akisi hazir
- Temel GitHub Actions CI pipeline'i mevcut
- Kubernetes base ve overlay dizinleri acildi, ancak implementasyon seviyesi halen erken asamada

## Next Steps

- Faz 1 servislerinin ilk implementasyonlarini genisletmek
- `frontend-web` icin calisan akisi tamamlamak
- Kubernetes base manifestlerini repo hedefleriyle tam uyumlu hale getirmek
- local ve staging overlay ayrimini netlestirmek
- Ingress, ConfigMap, Secret, liveness ve readiness probe kullanimini olgunlastirmak

## Notes

Bu repo bilerek tam production karmasikligina cikmaz. Buna karsin dosya organizasyonu, isimlendirme, servis sinirlari ve operasyonel kavramlar acisindan guven veren bir temel sunmayi hedefler.
