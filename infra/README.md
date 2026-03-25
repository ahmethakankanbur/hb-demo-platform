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

Bu klasör başlangıçta placeholder içerir; sonraki adımda gerçek manifestlerle doldurulacaktır.
