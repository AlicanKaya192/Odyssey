This exercise tests the trickiest part of the lesson.

Bring back only the `name` of products that are **in the `Accessory` or
`Display` category** and are **in stock**.

"In stock" means `stock` is above zero.

The result should be four rows.

`AND` runs before `OR`. Without parentheses the query means "every
Accessory, plus the Display items that are in stock" — which is not what you
want.

Watch the row count: forget the parentheses and you get five rows.
