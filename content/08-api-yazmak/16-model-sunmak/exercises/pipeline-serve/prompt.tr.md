Bu API hata vermiyor ama her çiçeğe aynı türü söylüyor: model ölçeklenmiş
veriyle eğitilmiş, sunumda ise ham ölçüler veriliyor.

**Yapman gereken:** `train_model`'ı ölçekleyiciyle modeli **tek bir hat**
(`make_pipeline(StandardScaler(), KNeighborsClassifier())`) olarak eğitecek
şekilde değiştir. Uç noktaya dokunma.

- `5.1, 3.5, 1.4, 0.2` → `setosa`
- `5.9, 3.0, 4.2, 1.5` → `versicolor`
- `6.7, 3.0, 5.2, 2.3` → `virginica`
