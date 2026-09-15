Bu bölümün yazımları ve hata metinleri tek sayfada. Sonuçlar Orta
Seviyenin sekiz tablolu şemasında ölçüldü.

## Görünüm

```sql
CREATE VIEW dbo.ad AS
SELECT sutun1, sutun2, hesap AS ad
FROM ...;                           -- ORDER BY yok

CREATE OR ALTER VIEW dbo.ad AS ...  -- varsa degistirir
DROP VIEW dbo.ad;

-- gorunumun WHERE'ine uymayan degisikligi reddeder
CREATE VIEW dbo.ad AS SELECT ... WHERE ... WITH CHECK OPTION;

-- tabloyu gorunum varken silinemez yapar; * yok, iki parcali ad
CREATE VIEW dbo.ad WITH SCHEMABINDING AS SELECT a, b FROM dbo.tablo;

-- SELECT * ile kurulmus gorunumu tablonun yeni hâline gore yeniler
EXEC sp_refreshview 'dbo.ad';
```

## Saklı yordam

```sql
CREATE PROCEDURE dbo.ad
    @p1 INT,                         -- zorunlu
    @p2 NVARCHAR(20) = N'pending',   -- varsayilanli
    @sonuc INT OUTPUT                -- cikis
AS
BEGIN
    SET NOCOUNT ON;
    ...
    RETURN 0;                        -- yalnizca tam sayi
END;

EXEC dbo.ad @p1 = 1, @sonuc = @x OUTPUT;   -- adiyla
EXEC dbo.ad 1, DEFAULT, @x OUTPUT;         -- sirasiyla
EXEC @durum = dbo.ad ...;                  -- RETURN degeri
DROP PROCEDURE dbo.ad;
```

## Hata vermek

```sql
IF <kosul>
    THROW 50001, N'Mesaj.', 1;       -- numara 50000 ve ustu

BEGIN TRY
    EXEC dbo.ad ...;
END TRY
BEGIN CATCH
    SELECT ERROR_NUMBER(), ERROR_MESSAGE(), ERROR_PROCEDURE();
END CATCH;
```

## Görünüm mü, yordam mı

| | Görünüm | Saklı yordam |
|---|---|---|
| parametre | yok | var |
| `FROM` içinde kullanım | evet | hayır (`Invalid object name`) |
| içinde `ORDER BY` | yalnızca `TOP` ile | serbest |
| birden fazla adım, `IF`, `THROW` | hayır | evet |
| veri değiştirmek | tek tablolu görünümden `UPDATE`/`INSERT` | içinde her şey |
| çağrı | `SELECT ... FROM dbo.ad` | `EXEC dbo.ad` |

## Veritabanında ne var

```sql
SELECT name, type_desc FROM sys.objects WHERE type IN ('V', 'P');
SELECT OBJECT_DEFINITION(OBJECT_ID('dbo.ad'));
SELECT name, is_output, has_default_value FROM sys.parameters
WHERE object_id = OBJECT_ID('dbo.ad');
SELECT TABLE_NAME, CHECK_OPTION FROM INFORMATION_SCHEMA.VIEWS;
```

## Hata metinleri

| Durum | Mesaj |
|---|---|
| `CREATE VIEW` ilk cümle değil | `'CREATE VIEW' must be the first statement in a query batch.` |
| `CREATE PROCEDURE` ilk cümle değil | `'CREATE/ALTER PROCEDURE' must be the first statement in a query batch.` |
| adsız sütun | `Create View or Function failed because no column name was specified for column 2.` |
| aynı ad | `There is already an object named '...' in the database.` |
| toplamalı görünümden yazmak | `Update or insert of view or function '...' failed because it contains a derived or constant field.` |
| `CHECK OPTION` ihlali | `The attempted insert or update failed because the target view either specifies WITH CHECK OPTION ...` |
| tablosu silinmiş görünüm | `Could not use view or function '...' because of binding errors.` |
| bağlı tabloyu silmek | `Cannot DROP TABLE '...' because it is being referenced by object '...'.` |
| eksik parametre | `Procedure or function '...' expects parameter '@...', which was not supplied.` |
| fazla parametre | `Procedure or function ... has too many arguments specified.` |
| yanlış tip | `Error converting data type varchar to int.` |
| `OUTPUT` olmayan parametreye `OUTPUT` | `The formal parameter "@x" was not declared as an OUTPUT parameter ...` |
| `THROW`'dan önce `;` yok | `Incorrect syntax near 'THROW'.` |
