Hatta yalnızca kod testleri var. Bir `model-gate` işi ekle:

- `test` bitince başlasın, makine `ubuntu-latest`.
- Adımlar sırayla: kodu çek (`actions/checkout@v4`); Python 3.13 kur (`actions/setup-python@v5`, `cache: pip`); `python -m pip install -r requirements.txt`; `python train.py`; `python check_quality.py`.
