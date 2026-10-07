MapReduce'u saf Python'la kurmak için iskelet ve Hadoop dünyasının
terimleri.

## İskelet

```python
from collections import defaultdict

def mapper(record):
    yield key, value                     # bir ya da birçok çift

def reducer(key, values):
    return key, sum(values)              # anahtarın değerlerinden tek sonuç

groups = defaultdict(list)               # shuffle
for record in records:
    for key, value in mapper(record):
        groups[key].append(value)

result = dict(reducer(k, v) for k, v in groups.items())
```

## Birleştirici (combiner)

Her makine (parça) göndermeden önce kendi çiftlerini topluyor:

```python
local = defaultdict(float)
for key, value in pairs:
    local[key] += value
# ağa yalnızca local'daki çiftler gidiyor
```

Bir milyon sipariş, 4 parça: 1 000 000 çift yerine 32.

## Bölümleyici (partitioner)

```python
import zlib

def partition(key, reducers):
    return zlib.crc32(key.encode()) % reducers
```

`hash()` kullanma: Python her süreçte metin karmasını farklı tohumla
hesaplıyor (`hash("Istanbul") % 4` beş süreçte 2, 1, 0, 2, 1 verdi).

## Sıralayarak gruplama

```python
from itertools import groupby

pairs.sort()
for key, group in groupby(pairs, key=lambda kv: kv[0]):
    total = sum(v for _, v in group)
```

`groupby` yalnızca yan yana duran aynı anahtarları birleştiriyor; önce
sırala.

## Hadoop terimleri

| Terim | Anlamı |
|---|---|
| **HDFS** | Hadoop'un dağıtık dosya sistemi |
| **Blok** | Dosyanın parçası; varsayılan 128 MB |
| **Kopya** (*replication*) | Her blok varsayılan üç makinede |
| **NameNode** | Hangi bloğun hangi makinede olduğunu bilen yönetici |
| **DataNode** | Blokları saklayan makine |
| **YARN** | Kümedeki işlemci ve belleği işlere dağıtan katman |
| **Hive** | MapReduce'un üstünde SQL |
| **Veri yerelliği** | Kodu verinin olduğu makinede çalıştırmak |
| **Veri çarpıklığı** (*skew*) | Bir makineye orantısız çok veri düşmesi |
