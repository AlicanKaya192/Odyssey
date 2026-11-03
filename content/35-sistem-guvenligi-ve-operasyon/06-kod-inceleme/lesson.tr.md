# Kod İnceleme ve Statik Analiz

Güvenli Yazılım Geliştirme bölümünde kodlama adımının güvenlik işlerinden
birinin **kod inceleme** olduğunu gördük. Bir değişiklik ana koda
girmeden önce en az bir kişi daha onu okur. İnceleme hataları erken
yakalar, bilgiyi ekibe yayar ve "bunu kimse görmedi" diye bir şey
bırakmaz.

İnsan gözü yorulur ve aynı şeyi bin kez aramak için uygun değildir. Bu
yüzden incelemenin yanında **statik analiz** (static analysis) kullanılır:
kodu **çalıştırmadan**, metnini ya da yapısını okuyarak hata arayan
araçlar. Bu bölüm ikisini birlikte anlatıyor ve Python'un `ast` modülüyle
küçük bir statik analiz aracı kuruyor. İncelenen kod parçaları yalnızca
metindir; hiçbiri çalıştırılmıyor.

## İnceleyen neye bakar?

| Soru | Örnek |
|---|---|
| Girdi nereden geliyor, doğrulanıyor mu? | Formdan gelen sayı aralık denetiminden geçiyor mu? |
| Yetki denetimi var mı, doğru yerde mi? | Her uç nokta sahipliği denetliyor mu? |
| Hata olunca ne oluyor? | Denetim hata olunca reddediyor mu? |
| Sır kodda mı? | Parola ya da anahtar dosyaya yazılmış mı? |
| Tehlikeli fonksiyon var mı? | `eval`, `exec`, güvensiz seri çözme |
| Ne **silindi**? | Değişiklik bir denetimi kaldırıyor mu? |

Son soru en kolay atlanandır: inceleyen eklenen satırlara odaklanır, oysa
bir güvenlik denetiminin sessizce silinmesi en tehlikeli değişikliktir.

## Metin aramak yetmez

En basit statik analiz metin aramaktır. `eval(` geçen satırları bulalım:

```python
SOURCE = '''# never call eval( on user input
note = "eval( is dangerous"
total = eval(expression)
'''
hits = [n for n, line in enumerate(SOURCE.splitlines(), 1) if "eval(" in line]
print(hits)
```

```text
[1, 2, 3]
```

Üç satır da yakalandı, ama yalnızca üçüncüsü gerçek bir çağrı: birincisi
yorum, ikincisi bir metin. Bunlara **yanlış alarm** (false positive) denir.
Çok yanlış alarm veren bir araç bir süre sonra dikkate alınmaz; bu da
gerçek bulguların kaçırılması demektir.

## Yapıya bakmak: sözdizimi ağacı

Python kodu çalıştırılmadan önce bir **soyut sözdizimi ağacına** (abstract
syntax tree, AST) çevrilir. `ast` modülü bu ağacı bize de verir. Ağaçta
yorumlar yoktur, metinler metin olarak durur ve bir fonksiyon çağrısı
`Call` düğümüdür. Aynı kaynağı ağaçla tarayalım:

```python
import ast

DANGEROUS = {"eval", "exec"}
for node in ast.walk(ast.parse(SOURCE)):
    if isinstance(node, ast.Call) and getattr(node.func, "id", "") in DANGEROUS:
        print(node.lineno, node.func.id)
```

```text
3 eval
```

Yalnızca gerçek çağrı bulundu. `ast.parse` kodu **çalıştırmaz**, yalnızca
yapısını çıkarır; bu yüzden incelenen kod ne kadar tehlikeli olursa olsun
analiz güvenlidir. Gerçek statik analiz araçları da aynı fikri çok daha
geniş kural listeleriyle uygular.

## Koddaki sırlar

Kaynak koda yazılmış bir parola, kodu görebilen herkese açıktır: depo
geçmişinde, yedeklerde, kopyalarda. Adı `password`, `secret` ya da `token`
içeren bir değişkene **sabit bir metin** atanmasını arayalım:

```python
import ast

CODE = '''
db_password = "hunter2"
api_token = load_from_vault("api")
retries = 3
SECRET_KEY = "dev-key-123"
'''
WORDS = ("password", "secret", "token")
for node in ast.walk(ast.parse(CODE)):
    if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant):
        if not isinstance(node.value.value, str):
            continue
        for target in node.targets:
            name = getattr(target, "id", "")
            if any(word in name.lower() for word in WORDS):
                print(node.lineno, name)
```

```text
2 db_password
5 SECRET_KEY
```

`db_password` ve `SECRET_KEY` sabit metinle atandığı için yakalandı.
`api_token` bir fonksiyondan (bir sır kasasından) geldiği için temiz
sayıldı; doğru yöntem de budur (Sır Yönetimi bölümü). `retries` bir sayı
ve adı şüpheli değil.

## Sessiz hata yutma

`except:` (türü yazılmamış yakalama) her hatayı yakalar. Güvenlik
denetiminin etrafında durursa, denetimin hatası sessizce yutulur ve kod
devam eder; bu, Güvenli Yazılım Geliştirme bölümündeki açık başarısızlığın
ta kendisidir:

```python
import ast

CODE = '''
try:
    check_permission(user)
except:
    pass
delete_everything()
'''
for node in ast.walk(ast.parse(CODE)):
    if isinstance(node, ast.ExceptHandler) and node.type is None:
        print("bare except at line", node.lineno)
```

```text
bare except at line 4
```

İzin denetimi hata verirse `pass` onu yutar ve sonraki satır yine çalışır.
Ağaçta türü olmayan yakalama `type` alanı `None` olan bir
`ExceptHandler`'dır; bulmak bu kadar kolaydır.

## Farka bakmak: ne silindi?

İnceleme çoğu zaman tüm dosyayı değil, değişikliğin **farkını** (diff)
okur. Farkta `+` ile başlayan satırlar eklenen, `-` ile başlayanlar silinen
satırlardır:

```python
DIFF = """--- a/app.py
+++ b/app.py
@@ -10,3 +10,4 @@
 def save(user, data):
-    check_owner(user, data)
+    log(user)
     store(data)
+    return True
"""
lines = DIFF.splitlines()
removed = [l[1:].strip() for l in lines if l.startswith("-") and not l.startswith("---")]
added = [l[1:].strip() for l in lines if l.startswith("+") and not l.startswith("+++")]
print("removed:", removed)
print("added:", added)
```

```text
removed: ['check_owner(user, data)']
added: ['log(user)', 'return True']
```

Eklenen iki satır zararsız görünüyor. Asıl önemli olan silinen satır:
sahiplik denetimi kaldırılmış. Bu değişiklik onaylanırsa yatay yetki
yükseltmeye (Yetki Yükseltme bölümü) kapı açılır. İnceleyen önce silinen
satırlara bakar.

## Araç ile insan

<figure class="fig"><div class="versus">
  <div><h4>Statik analiz aracı</h4>Yorulmaz, her değişiklikte aynı kuralları uygular, bilinen kalıpları (tehlikeli fonksiyon, koddaki sır) hızla bulur. Ama <b>niyeti</b> bilmez ve yanlış alarm verir.</div>
  <div><h4>İnsan inceleyici</h4>Kodun ne yapmaya çalıştığını anlar, eksik bir denetimi ya da mantık hatasını görür. Ama yorulur ve aynı şeyi bin kez arayamaz.</div>
</div><figcaption>İkisi birbirinin yerini tutmaz; araç kalıpları, insan anlamı denetler.</figcaption></figure>

Araçlar derleme hattına (CI) konur ve her değişiklikte kendiliğinden
çalışır. Bir bulgu bilerek kabul edilecekse (gerçekten yanlış alarmsa) bu,
kodun içinde gerekçesiyle işaretlenir; sessizce görmezden gelinmez.

## Özet

- **Kod inceleme:** değişiklik ana koda girmeden önce başka biri okur;
  girdi, yetki, hata durumu, sırlar ve **silinen satırlar** sorulur.
- **Statik analiz:** kodu çalıştırmadan okuyarak hata arar.
- Metin araması yorumları ve metinleri de yakalar: **yanlış alarm**.
- **AST** kodun yapısını verir; `ast.parse` kodu çalıştırmaz.
- Sabit metinle atanan sırlar, türsüz `except:` ve tehlikeli çağrılar
  ağaçla kolayca bulunur.
- Araç kalıpları, insan anlamı denetler; ikisi birlikte kullanılır.
