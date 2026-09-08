This exercise tests the trickiest part of the lesson.

Bring back only the `ad` of products that are **in the `Aksesuar` or
`Ekran` category** and are **in stock**.

"In stock" means `stok` is above zero.

The result should be four rows.

`AND` runs before `OR`. Without parentheses the query means "every
Aksesuar, plus the Ekran items that are in stock" — which is not what you
want.

Watch the row count: forget the parentheses and you get five rows.
