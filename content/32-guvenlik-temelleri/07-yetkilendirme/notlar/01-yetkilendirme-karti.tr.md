## Terimler

| Terim | Anlamı |
|---|---|
| **Özne** (subject) | İşi yapmak isteyen: kullanıcı, program, hizmet |
| **Nesne / kaynak** (object, resource) | Üzerinde iş yapılan şey |
| **Eylem** (action) | Okumak, yazmak, silmek, onaylamak |
| **Erişim denetim matrisi** | Satır özne, sütun nesne, hücre izinli eylemler |
| **ACL** (access control list) | Matrisin sütunu: nesnenin yanında kim ne yapabilir |
| **Yetenek listesi** (capability list) | Matrisin satırı: öznenin yanında neye ne yapabilir |
| **IDOR** | Nesne düzeyinde denetim unutulunca başkasının nesnesine ulaşmak |
| **Yatay aşım** | Aynı düzeydeki başka kullanıcının verisine ulaşmak |
| **Dikey aşım / yetki yükseltme** | Daha yüksek bir yetkiyi kullanmak |

## Karar cümlesi

"**Özne**, **nesne** üzerinde **eylemi** yapabilir mi?" Cevap yoksa: hayır.

## Python kalıbı

```python
def is_allowed(matrix, subject, obj, action):
    return action in matrix.get(subject, {}).get(obj, [])
```

İç içe `get` her düzeyde varsayılan verir: bilinmeyen özne de bilinmeyen
nesne de boş listeye düşer, yani reddedilir.

## Denetim listesi

- Karar sunucuda mı veriliyor?
- Her uç nokta aynı karar fonksiyonunu mu çağırıyor?
- "Bu nesne kimin?" sorusu soruluyor mu?
- Rol istemciden değil sunucudaki kayıttan mı okunuyor?
- Reddedilen istekler kayda geçiyor mu?
