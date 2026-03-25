# ADR-0001: Öğrenme Odaklı Production-Minded Monorepo

## Durum

Kabul edildi.

## Bağlam

Repo hem DevOps öğrenme ortamı hem de GitHub portföy projesi olarak kullanılacaktır. Bu nedenle yapı hem sade hem de profesyonel görünmelidir.

## Karar

Tek repo içinde servisler, altyapı dosyaları, dokümantasyon ve scriptler ayrı klasörlerde tutulacaktır.

Seçilen ana yapı:

- `services/`
- `infra/`
- `docs/`
- `scripts/`
- `.github/workflows/`

## Sonuçlar

### Pozitif

- Navigasyonu kolaylaştırır.
- CI/CD ve deployment dosyalarını uygulama kodundan ayırır.
- Portföy açısından okunabilirlik sağlar.

### Negatif

- İlk aşamada bazı klasörler placeholder olarak boş görünür.
- Gerçek servis implementasyonu gelene kadar yapı kısmen teorik kalır.
