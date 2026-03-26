# kubernetes base

Ortamdan bağımsız temel Kubernetes manifestleri burada tutulur.

Bu base set şu kaynakları içerir:

- `namespace.yaml`: tüm kaynakları `hb-demo` namespace'i altında toplar
- `api-gateway`, `catalog-service`, `cart-service` için birer `Deployment`
- her servis için birer dahili `Service`
- `api-gateway-configmap.yaml`: gateway'in upstream servis URL'leri ve timeout ayarları
- `api-gateway-ingress.yaml`: gelen HTTP trafiğini `api-gateway` servisine yönlendiren sade ingress

Amaç, local veya staging overlay'lerinin üzerine çıkabileceği sade ve çalışır bir başlangıç seti vermektir.
