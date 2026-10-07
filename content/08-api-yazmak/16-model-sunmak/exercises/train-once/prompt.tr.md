`train_model()` hazır: iris verisiyle bir model eğitiyor ve
`stats["trainings"]`'i artırıyor. (Gerçekte burada `joblib.load` olurdu;
alıştırmada dosya yerine eğitiyoruz, 0,05 sn sürüyor.)

**Yapman gerekenler:**

1. `lifespan`: açılışta `ml["model"] = train_model()` (**bir kez**),
   kapanışta `ml.clear()`.
2. `GET /model` → `{"type": "LogisticRegression", "features": 4, "classes": [...]}`
3. `GET /stats` → `stats`; birkaç istekten sonra da `{"trainings": 1}`.
