SELECT id, created_at, amount
FROM events
WHERE event_type = N'purchase'
  AND created_at >= '2025-06-01'
  AND created_at <  '2025-06-02'
ORDER BY created_at;
