Depoda `cart.py`, testleri (`test_cart.py`) ve `requirements.txt` var.

İş akışını tamamla:

- Hem `push` hem `pull_request` olayında çalışsın: `on: [push, pull_request]`
- Kodu indirdikten sonra Python **3.13**'ü kursun (`actions/setup-python@v5`, `with:` altında `python-version: "3.13"`)
- `pip install -r requirements.txt` ile bağımlılıkları kursun
- `python -m pytest` ile testleri çalıştırsın
