This time we sort on two criteria.

Sort the products **alphabetically by category first**, then **from
expensive to cheap inside each category**. Columns: `category`, `name`,
`price`.

```
category   name      price 
---------  --------  ------
Accessory  Webcam    1150.0
Accessory  Headset   890.0 
Accessory  Keyboard  450.0 
Accessory  Mouse     220.0 
...
```

The thing to watch: `DESC` applies only to the column it is written on.
The category stays ascending, the price becomes descending.
