This section's syntax and error messages on one page. The results were
measured on the eight-table schema of the Intermediate level.

## A view

```sql
CREATE VIEW dbo.name AS
SELECT column1, column2, calculation AS name
FROM ...;                           -- no ORDER BY

CREATE OR ALTER VIEW dbo.name AS ...  -- changes it if it exists
DROP VIEW dbo.name;

-- refuses changes that do not meet the view's WHERE
CREATE VIEW dbo.name AS SELECT ... WHERE ... WITH CHECK OPTION;

-- the table cannot be dropped while the view exists; no *, two-part names
CREATE VIEW dbo.name WITH SCHEMABINDING AS SELECT a, b FROM dbo.table_name;

-- refreshes a view built with SELECT * to the table's current shape
EXEC sp_refreshview 'dbo.name';
```

## A stored procedure

```sql
CREATE PROCEDURE dbo.name
    @p1 INT,                         -- required
    @p2 NVARCHAR(20) = N'pending',   -- with a default
    @result INT OUTPUT               -- output
AS
BEGIN
    SET NOCOUNT ON;
    ...
    RETURN 0;                        -- whole numbers only
END;

EXEC dbo.name @p1 = 1, @result = @x OUTPUT;   -- by name
EXEC dbo.name 1, DEFAULT, @x OUTPUT;          -- by position
EXEC @status = dbo.name ...;                  -- the RETURN value
DROP PROCEDURE dbo.name;
```

## Raising an error

```sql
IF <condition>
    THROW 50001, N'Message.', 1;     -- numbers from 50000 up

BEGIN TRY
    EXEC dbo.name ...;
END TRY
BEGIN CATCH
    SELECT ERROR_NUMBER(), ERROR_MESSAGE(), ERROR_PROCEDURE();
END CATCH;
```

## A view or a procedure

| | View | Stored procedure |
|---|---|---|
| parameters | none | yes |
| used inside `FROM` | yes | no (`Invalid object name`) |
| `ORDER BY` inside | only with `TOP` | freely |
| several steps, `IF`, `THROW` | no | yes |
| changing data | `UPDATE`/`INSERT` through a single-table view | anything inside |
| call | `SELECT ... FROM dbo.name` | `EXEC dbo.name` |

## What is in the database

```sql
SELECT name, type_desc FROM sys.objects WHERE type IN ('V', 'P');
SELECT OBJECT_DEFINITION(OBJECT_ID('dbo.name'));
SELECT name, is_output, has_default_value FROM sys.parameters
WHERE object_id = OBJECT_ID('dbo.name');
SELECT TABLE_NAME, CHECK_OPTION FROM INFORMATION_SCHEMA.VIEWS;
```

## Error messages

| Situation | Message |
|---|---|
| `CREATE VIEW` not the first statement | `'CREATE VIEW' must be the first statement in a query batch.` |
| `CREATE PROCEDURE` not the first statement | `'CREATE/ALTER PROCEDURE' must be the first statement in a query batch.` |
| an unnamed column | `Create View or Function failed because no column name was specified for column 2.` |
| the same name | `There is already an object named '...' in the database.` |
| writing through an aggregating view | `Update or insert of view or function '...' failed because it contains a derived or constant field.` |
| a `CHECK OPTION` violation | `The attempted insert or update failed because the target view either specifies WITH CHECK OPTION ...` |
| a view whose table was dropped | `Could not use view or function '...' because of binding errors.` |
| dropping a bound table | `Cannot DROP TABLE '...' because it is being referenced by object '...'.` |
| a missing parameter | `Procedure or function '...' expects parameter '@...', which was not supplied.` |
| too many parameters | `Procedure or function ... has too many arguments specified.` |
| a wrong type | `Error converting data type varchar to int.` |
| `OUTPUT` on a parameter not declared as one | `The formal parameter "@x" was not declared as an OUTPUT parameter ...` |
| no `;` before `THROW` | `Incorrect syntax near 'THROW'.` |
