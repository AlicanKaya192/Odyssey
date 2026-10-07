# min_gap(allowed, window_seconds): seconds, two decimals
# job_minutes(total_requests, allowed, window_seconds): minutes, one decimal


jobs = [
    (500, 60, 60),      # 500 requests, 60 a minute
    (120, 3, 1),        # 120 requests, 3 a second
    (10000, 1000, 3600),  # 10,000 requests, 1000 an hour
]
# Each job: "500 requests: gap 1.0 s, at least 8.3 min"
