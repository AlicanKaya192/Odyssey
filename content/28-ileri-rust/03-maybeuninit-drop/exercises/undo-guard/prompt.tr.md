`add_all(list, items)`: Öğeleri ekle. Boş öğede `Err("empty item")` dön ve o ana kadar eklenenler silinsin. Bunu `Undo` koruyucusuyla yap: `Drop` listeyi `keep`'e kısaltsın, başarıda `mem::forget`.
