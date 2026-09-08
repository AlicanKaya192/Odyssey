From this section on you are working with an **eight-table** order
database. You can see all of them with the **Tables** button.

The `products` table only holds the category's **code** (`ACC`, `DIS`...);
the name lives in the `categories` table.

Return each product's name and the **name** of its category.

Columns: `product` and `category`. Sort by product name.

```
product    category 
---------  ---------
Antivirus  Software 
Cable      Accessory
...
```

The result should be twelve rows — every product has a category recorded.

**Careful:** both tables have a column called `name`. If you do not say
which one you mean you will get `Ambiguous column name`.
