Yanında `notes.txt` var. `backup_file(path, folder)` fonksiyonunu yaz:
`folder` klasörünü (aradakilerle birlikte) açsın, dosyayı zamanını koruyarak
(`shutil.copy2`) içine kopyalasın ve yeni dosyanın yolunu `/` ayıraçlı metin
olarak döndürsün (`Path(...).as_posix()`).

**Beklenen çıktı:**

```
backup/notes.txt
Meeting at 10.
```
