"""minilog: a tiny, single-process imitation of a Kafka topic.

A topic is split into partitions; each partition is an append-only log.
Every record gets an offset: its position in its partition (0, 1, 2, ...).
Records with the same key always go to the same partition, so their order
is kept. Consumers do not delete what they read; they remember where they
are (the offset) and continue from there.

Read only: you import it, you do not change it.
"""
import zlib


class Topic:
    def __init__(self, name, partitions=3):
        self.name = name
        self._logs = [[] for _ in range(partitions)]

    @property
    def partitions(self):
        return len(self._logs)

    def partition_for(self, key):
        """The partition of a key: the same key always gives the same number."""
        return zlib.crc32(str(key).encode("utf-8")) % len(self._logs)

    def send(self, key, value):
        """Appends a record and returns (partition, offset)."""
        p = self.partition_for(key)
        log = self._logs[p]
        log.append((key, value))
        return p, len(log) - 1

    def end_offset(self, partition):
        """The offset the next record in this partition will get."""
        return len(self._logs[partition])

    def read(self, partition, offset, max_records=100):
        """Up to max_records records from offset on: [(offset, key, value), ...]."""
        log = self._logs[partition]
        end = min(offset + max_records, len(log))
        return [(i, log[i][0], log[i][1]) for i in range(offset, end)]
