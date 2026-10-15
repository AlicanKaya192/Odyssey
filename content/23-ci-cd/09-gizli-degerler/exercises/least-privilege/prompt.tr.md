Bu hat etiket gelince test edip bir GitHub sürümü açıyor ama hiç izin yazılmamış; `GITHUB_TOKEN` deponun varsayılanı kadar geniş. İzinleri daralt:

- İş akışının en üstünde bütün işler için `contents: read`.
- Yalnızca `release` işi `contents: write` alsın (sürüm açmak için).
