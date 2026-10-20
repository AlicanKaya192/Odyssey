İş akışında yalnızca testler var ve yalnızca elle başlıyor. Hattı her ay çalıştır:

- Tetikleyicilere her ayın 1'inde **03:00 UTC** (`schedule`) ekle; `workflow_dispatch` kalsın.
- Bir `retrain` işi ekle: `test` bitince başlasın, `ubuntu-latest`, `timeout-minutes: 30`.
- Adımlar sırayla: kodu çek (`actions/checkout@v4`); Python 3.13 kur (`actions/setup-python@v5`, `cache: pip`); `python -m pip install -r requirements.txt`; `python pipeline.py`; raporu **her durumda** sakla (`actions/upload-artifact@v4`, `name: pipeline-report`, `path: report.txt`).
