Hat yalnızca `main`'e gönderimde çalışıyor; PR'lar sınanmadan birleştiriliyor. Tetikleyicilere iki olay ekle:

- `main`'e açılan PR'lar: `pull_request`, `branches: [main]`.
- Birleştirme kuyruğu: `merge_group`.
