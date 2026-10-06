limit = 30

best_start = 0
best_steps = 0

# Dış döngü: 1'den limit'e kadar her başlangıç sayısı
#   n = start, steps = 0
#   İç döngü (while): n 1 olana kadar kuralı uygula, adımları say
#   Bu yolculuk şimdiye kadarkinden uzunsa best_start ve best_steps'i güncelle


print("Longest:", best_start, "with", best_steps, "steps")
