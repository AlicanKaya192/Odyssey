Her çalışanın şirketteki **kademesini** bul: yöneticisi olmayan en
üstteki kişi 0, onun doğrudan altındakiler 1, onların altındakiler 2.

Sütunlar: `id`, `name`, `level`. Önce `level`, sonra `id` ile sırala.

```
id  name         level
--  -----------  -----
1   Ada Kilic    0
2   Bora Yilmaz  1
5   Emre Sahin   1
3   Ceren Aksoy  2
...
```

`employees` tablosunda her çalışanın `manager_id`'si var. Kaç kademe
olduğunu bilmeden yazılması gereken bir sorgu bu: özyinelemeli bir
`WITH` en üstteki kişiden başlayıp her adımda bir kat aşağı iniyor ve
yeni kimse gelmeyince duruyor.
