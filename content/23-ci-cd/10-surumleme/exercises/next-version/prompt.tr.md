`next_version(version, messages)` fonksiyonunu yaz. Son sürümün numarasını ve o zamandan beri gelen commit mesajlarını alsın, sıradaki sürüm numarasını döndürsün.

Her mesajın **öneki** ilk `:` işaretinden önceki kısımdır (`:` yoksa mesajın tamamı).

- Önek `!` ile bitiyorsa ya da mesajda `BREAKING CHANGE` geçiyorsa: ANA (`major`)
- Değilse, önek `feat` ile başlıyorsa: YAN (`minor`)
- Değilse, önek `fix` ile başlıyorsa: YAMA (`patch`)
- Diğerleri sürümü değiştirmez.

Mesajların **en büyüğü** kazanır. Hiçbiri sürümü değiştirmiyorsa numara aynen döner. Numarayı artırmak için hazır `bump` fonksiyonunu kullan.

**Beklenen çıktı:**

```
1.4.3
1.5.0
2.0.0
1.4.2
1.0.0
```
