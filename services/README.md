# services

Bu klasör iş alanına göre ayrılmış uygulama servislerini içerir.

## Tasarım İlkeleri

- Her servis kendi sorumluluğuna sahip olur.
- Her servis zamanla kendi `Dockerfile`, `Makefile`, testleri ve uygulama koduna sahip olabilir.
- İlk etapta README ve placeholder yapısı ile sınırlar netleştirilir.

## Fazlar

### Faz 1

- `frontend-web`
- `api-gateway`
- `catalog-service`
- `cart-service`

### Faz 2

- `order-service`
- `identity-service`

Amaç, önce çalışan bir demo akışı kurup sonra servis sayısını artırmaktır.
