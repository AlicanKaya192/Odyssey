## Diziler

| Yazım | Ne |
|---|---|
| `nn.Embedding(V, D, padding_idx=0)` | kimlik → vektör, dolgu kimliğinin vektörü sıfır |
| `nn.LSTM(D, H, batch_first=True)` | girdi `(B, T, D)`; çıkış ve `(h, c)` |
| `pack_padded_sequence(x, lengths, batch_first=True, enforce_sorted=False)` | dolguyu atlatmak |
| `nn.Conv1d(C, K, kernel_size, dilation=d)` | girdi `(B, C, T)`; genişletilmiş evrişim |
| `x.transpose(1, 2)` | `(B, T, D)` → `(B, D, T)` |
| `torch.triu(torch.ones(T, T, dtype=torch.bool), 1)` | nedensel maske (gelecek `True`) |
| `nn.TransformerEncoder(layer, num_layers)` | kodlayıcı bloklarını üst üste koymak |

## Üretken modeller

| Yazım | Ne |
|---|---|
| `F.mse_loss(model(x), x)` | otomatik kodlayıcının kaybı |
| `mu + torch.exp(0.5 * logvar) * torch.randn_like(mu)` | yeniden parametreleme |
| `-0.5 * torch.mean(torch.sum(1 + logvar - mu ** 2 - logvar.exp(), dim=1))` | KL terimi |
| `loss_fn(D(real), ones) + loss_fn(D(fake.detach()), zeros)` | ayırt edicinin kaybı |
| `loss_fn(D(fake), ones)` | üreticinin kaybı |

## Az etiket

| Yazım | Ne |
|---|---|
| `F.normalize(z, dim=1)`; `z @ z.T / tau` | kosinüs benzerliği / sıcaklık |
| `sim.fill_diagonal_(float("-inf"))` | kendisiyle benzerliği adaylardan çıkarmak |
| `F.cross_entropy(sim, target)` | NT-Xent |
| `base.requires_grad_(False)` | dondurmak |
| `x @ A.T @ B.T * (alpha / r)` | LoRA'nın katkısı |
| `W + (alpha / r) * B @ A` | uyarlamayı ağırlığa katmak |

## Dağıtım

| Yazım | Ne |
|---|---|
| `time.perf_counter()`, en kısası | süre ölçmek |
| `torch.inference_mode()` | tahmin: grafik yok |
| `torch.autocast("cpu", dtype=torch.bfloat16)` | karışık duyarlık |
| `record_function("ad")` + `profile(...)` | profil |
| `torch.export.export(m, (x,), dynamic_shapes=({0: Dim("batch")},))` | dışa aktarmak |
| `torch.export.save` / `torch.export.load(...).module()` | `.pt2` kaydet / yükle |
| `torch.cond(koşul, f, g, (x,))` | dışa aktarılabilir dallanma |
| `torch.round(w / scale).clamp(-127, 127).to(torch.int8)` | `int8` nicemleme |
| `prune.l1_unstructured(m, "weight", amount=0.5)` | budama |
| `random.seed`, `np.random.seed`, `torch.manual_seed` | tohumlar |
| `DataLoader(..., generator=torch.Generator().manual_seed(s))` | tohumlu karıştırma |
| `torch.use_deterministic_algorithms(True)` | deterministik işlemler |

## Ölçmek

| Durum | Ölçü |
|---|---|
| Dengeli sınıflar | doğruluk |
| Azınlık sınıfı (arıza, anomali) | kesinlik, duyarlılık; eşik bedele göre |
| Tahmin (sayı) | MAE; taban çizgisine karşı |
| Üretken model | üretilen örneklerin kendisi (ör. öbek payları) |
| Etiketsiz öğrenme | en yakın komşu doğruluğu, doğrusal yoklama |
| Küçültülmüş model | özgün modelle doğruluk farkı |
| Dışa aktarılmış model | altın çıktı (`allclose`) |
