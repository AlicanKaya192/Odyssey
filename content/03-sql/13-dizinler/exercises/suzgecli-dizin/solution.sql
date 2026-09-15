CREATE INDEX ix_events_amount ON events (amount) WHERE amount IS NOT NULL;
