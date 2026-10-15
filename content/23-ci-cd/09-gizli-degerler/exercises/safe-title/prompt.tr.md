Bu iş PR'ın başlığını ve dal adını yazdırıyor, ama ikisi de `run:` satırına `${{ }}` ile doğrudan yazılmış: PR'ı açan kişi başlığa ya da dal adına komut koyabilir. İkisini de ortam değişkeninden ver:

- Başlık `TITLE` değişkeninde, komut `echo "Checking PR $TITLE"`.
- Dal adı `BRANCH` değişkeninde, komut `echo "From branch $BRANCH"`.
