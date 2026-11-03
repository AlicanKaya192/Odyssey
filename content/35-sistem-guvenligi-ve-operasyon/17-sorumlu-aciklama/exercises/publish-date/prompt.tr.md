`publish_date(reported, fixed, deadline_days, grace_days)` duyuru gününü
ISO metin olarak döndürsün: son tarih bildirim günü + `deadline_days`.
Düzeltme günü (`fixed`) varsa düzeltme + `grace_days` ile son tarihten
hangisi önceyse o; düzeltme yoksa (`None`) son tarih.

**Beklenen çıktı:**

```
2027-01-24
2027-02-01
2027-02-01
```
