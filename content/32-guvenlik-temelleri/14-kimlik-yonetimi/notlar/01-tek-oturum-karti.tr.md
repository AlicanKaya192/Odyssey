## Terimler

| Terim | Tek satır |
|---|---|
| IAM | Kimlik ve erişim yönetimi: kim, neye, ne zamana kadar |
| Dizin (directory) | Kişilerin, grupların ve rollerin tek kaynağı; erişim standardı LDAP |
| SSO | Bir kez giriş, birçok uygulama |
| IdP | Kimlik sağlayıcı: girişin yapıldığı yer, parolayı yalnızca o görür |
| SP | Hizmet sağlayıcı: kullanılan uygulama, imzalı jetona güvenir |
| Federasyon | Farklı kurumların birbirinin kimliğine güvenmesi |
| SAML 2.0 | Kurumsal SSO, XML onay (assertion) |
| OAuth 2.0 | Yetki devri, erişim jetonu |
| OpenID Connect | OAuth üstüne kimlik, kimlik jetonu (JWT) |

## Jeton denetimi sırası

1. Biçim doğru mu? (parça sayısı)
2. **İmza** doğru mu? Algoritmayı sunucu belirler; `none` kabul edilmez.
3. `iss`: güvendiğimiz IdP mi?
4. `aud`: bizim uygulamamız için mi?
5. `exp`: süresi dolmamış mı?
6. `nbf`: geçerlilik başlamış mı?
7. Ancak bunlardan sonra içerikteki rol ya da yetki kullanılır.

## Akılda tutulacaklar

- İmza **gizlemez**, yalnızca değişmediğini kanıtlar; jetona sır konmaz.
- Erişim jetonu kısa ömürlü; uzun oturum için iptal edilebilen yenileme
  jetonu.
- İmza karşılaştırması sabit süreli: `hmac.compare_digest`.
- IdP tek hedeftir: güçlü çok faktörlü doğrulama ve sıkı izleme.
- "OAuth ile giriş" denince kastedilen çoğu zaman OpenID Connect'tir.
