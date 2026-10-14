`render_chat(messages)` mesaj listesini tek bir metne çevirsin: her mesaj için
`<rol>` işareti ve içerik, aralarında birer boşluk; en sonda `<assistant>`.
Örneğin `[{"role": "user", "content": "hi !"}]` için
`"<user> hi ! <assistant>"`.

**Beklenen çıktı:**

```
<system> be brief . <user> hi <assistant>
```
