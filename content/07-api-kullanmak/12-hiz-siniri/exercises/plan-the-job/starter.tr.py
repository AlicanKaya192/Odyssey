# min_gap(allowed, window_seconds): saniye, iki ondalik
# job_minutes(total_requests, allowed, window_seconds): dakika, bir ondalik


jobs = [
    (500, 60, 60),      # 500 istek, dakikada 60
    (120, 3, 1),        # 120 istek, saniyede 3
    (10000, 1000, 3600),  # 10 000 istek, saatte 1000
]
# Her is: "500 requests: gap 1.0 s, at least 8.3 min"
