`split(cidr, new_prefix)` ağı `new_prefix` önekli eşit parçalara
bölsün ve parçaları metin olarak (`"192.168.1.0/26"`) bir liste hâlinde
döndürsün. `ipaddress.ip_network(cidr).subnets(new_prefix=...)` parçaları
verir; her birini `str` ile metne çevir.

**Beklenen çıktı:**

```
192.168.1.0/26
192.168.1.64/26
192.168.1.128/26
192.168.1.192/26
256
```
