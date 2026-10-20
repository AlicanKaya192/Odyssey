Toplu tahmin iş akışı yalnızca elle başlıyor ve skorları üretmiyor. Tamamla:

- Her gece **02:00 UTC**'de çalışsın (`schedule`); `workflow_dispatch` kalsın.
- `score` işine `timeout-minutes: 20` ekle.
- Kurulumdan sonra `python score.py` çalıştır ve sonucu sakla: `actions/upload-artifact@v4`, `name: scores`, `path: scores.csv`.
