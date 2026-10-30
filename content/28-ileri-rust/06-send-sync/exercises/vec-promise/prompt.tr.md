`MyVec<T>` `NonNull` tuttuğu için kola geçmiyor. `T: Send` şartıyla `Send`, `T: Sync` şartıyla `Sync` yaz. `// SAFETY:` yorumu ekle.
