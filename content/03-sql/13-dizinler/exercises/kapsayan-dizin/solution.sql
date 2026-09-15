CREATE INDEX ix_events_created ON events (created_at) INCLUDE (amount);
