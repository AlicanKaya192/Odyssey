"""minispark: a tiny, single-machine imitation of PySpark for learning.

Real Spark runs on a cluster and needs Java. This module runs inside one
Python process, but it keeps Spark's names and its main ideas:

- data is split into partitions,
- transformations are lazy and only record a lineage,
- actions run the lineage partition by partition,
- reduceByKey combines inside each partition, then shuffles by key,
- DataFrames run their plan partition by partition and can be queried
  with SQL.

Read only: you import it, you do not change it.
"""
import zlib
from collections import defaultdict

import duckdb
import pandas as pd


def _bucket(key, n):
    """Stable partition number for a key (same in every process)."""
    return zlib.crc32(repr(key).encode()) % n


class _Stats:
    def __init__(self):
        self.partitions_computed = 0
        self.jobs = 0
        self.shuffles = 0


class SparkContext:
    def __init__(self):
        self.stats = _Stats()

    def parallelize(self, data, numSlices=2):
        data = list(data)
        size = len(data)
        parts = []
        for i in range(numSlices):
            start = size * i // numSlices
            stop = size * (i + 1) // numSlices
            parts.append(data[start:stop])
        return RDD(self, source=parts, name="parallelize")


class RDD:
    def __init__(self, sc, source=None, parent=None, fn=None, name="", wide=False):
        self.sc = sc
        self._source = source
        self._parent = parent
        self._fn = fn
        self._name = name
        self._wide = wide
        self._cache = None
        self._cache_wanted = False

    # ---- running ----------------------------------------------------
    def _partitions(self):
        if self._cache is not None:
            return self._cache
        if self._source is not None:
            parts = [list(p) for p in self._source]
        else:
            parts = self._fn(self._parent._partitions())
        self.sc.stats.partitions_computed += len(parts)
        if self._cache_wanted:
            self._cache = parts
        return parts

    def _narrow(self, per_partition, name):
        return RDD(self.sc, parent=self, name=name,
                   fn=lambda parts: [per_partition(p) for p in parts])

    # ---- transformations (lazy) ---------------------------------------
    def map(self, f):
        return self._narrow(lambda p: [f(x) for x in p], "map")

    def filter(self, f):
        return self._narrow(lambda p: [x for x in p if f(x)], "filter")

    def flatMap(self, f):
        return self._narrow(lambda p: [y for x in p for y in f(x)], "flatMap")

    def mapValues(self, f):
        return self._narrow(lambda p: [(k, f(v)) for k, v in p], "mapValues")

    def keys(self):
        return self._narrow(lambda p: [k for k, _ in p], "keys")

    def values(self):
        return self._narrow(lambda p: [v for _, v in p], "values")

    def _shuffle(self, parts, n):
        self.sc.stats.shuffles += 1
        out = [[] for _ in range(n)]
        for p in parts:
            for k, v in p:
                out[_bucket(k, n)].append((k, v))
        return out

    def reduceByKey(self, f, numPartitions=None):
        def run(parts):
            n = numPartitions or len(parts)
            combined = []
            for p in parts:
                local = {}
                for k, v in p:
                    local[k] = f(local[k], v) if k in local else v
                combined.append(list(local.items()))
            result = []
            for p in self._shuffle(combined, n):
                acc = {}
                for k, v in p:
                    acc[k] = f(acc[k], v) if k in acc else v
                result.append(list(acc.items()))
            return result
        return RDD(self.sc, parent=self, fn=run, name="reduceByKey", wide=True)

    def groupByKey(self, numPartitions=None):
        def run(parts):
            n = numPartitions or len(parts)
            result = []
            for p in self._shuffle(parts, n):
                groups = defaultdict(list)
                for k, v in p:
                    groups[k].append(v)
                result.append(list(groups.items()))
            return result
        return RDD(self.sc, parent=self, fn=run, name="groupByKey", wide=True)

    def distinct(self):
        return self.map(lambda x: (x, None)).reduceByKey(lambda a, b: a).keys()

    def sortBy(self, f, ascending=True):
        def run(parts):
            items = sorted((x for p in parts for x in p), key=f, reverse=not ascending)
            n = len(parts)
            size = len(items)
            return [items[size * i // n:size * (i + 1) // n] for i in range(n)]
        return RDD(self.sc, parent=self, fn=run, name="sortBy", wide=True)

    def cache(self):
        self._cache_wanted = True
        return self

    persist = cache

    # ---- actions (run the lineage) ------------------------------------
    def _run(self):
        self.sc.stats.jobs += 1
        return self._partitions()

    def collect(self):
        return [x for p in self._run() for x in p]

    def count(self):
        return sum(len(p) for p in self._run())

    def take(self, n):
        return self.collect()[:n]

    def first(self):
        return self.take(1)[0]

    def reduce(self, f):
        items = self.collect()
        result = items[0]
        for x in items[1:]:
            result = f(result, x)
        return result

    def sum(self):
        return sum(self.collect())

    def glom(self):
        return self._narrow(lambda p: [p], "glom")

    def getNumPartitions(self):
        rdd = self
        while rdd._source is None and not rdd._wide:
            rdd = rdd._parent
        if rdd._source is not None:
            return len(rdd._source)
        return len(rdd._partitions())

    def toDebugString(self):
        lines = []
        rdd = self
        depth = 0
        while rdd is not None:
            mark = " (shuffle)" if rdd._wide else ""
            lines.append("  " * depth + "+- " + rdd._name + mark)
            rdd = rdd._parent
            depth += 1
        return "\n".join(lines)


class GroupedData:
    def __init__(self, df, keys):
        self._df = df
        self._keys = keys

    def agg(self, spec):
        keys = self._keys

        def run(parts):
            partial = []
            for p in parts:
                g = p.groupby(keys)
                cols = {}
                for col, how in spec.items():
                    if how == "avg":
                        cols[col + "__sum"] = g[col].sum()
                        cols[col + "__count"] = g[col].count()
                    elif how == "count":
                        cols[col + "__count"] = g[col].count()
                    else:
                        cols[col + "__" + how] = getattr(g, "__getitem__")(col).agg(how)
                partial.append(pd.DataFrame(cols).reset_index())
            joined = pd.concat(partial, ignore_index=True)
            g = joined.groupby(keys)
            out = pd.DataFrame(index=g.size().index)
            for col, how in spec.items():
                if how == "avg":
                    out[f"avg({col})"] = g[col + "__sum"].sum() / g[col + "__count"].sum()
                elif how == "count":
                    out[f"count({col})"] = g[col + "__count"].sum()
                elif how == "sum":
                    out[f"sum({col})"] = g[col + "__sum"].sum()
                else:
                    out[f"{how}({col})"] = g[col + "__" + how].agg(how)
            return [out.reset_index()]

        return DataFrame(self._df._session, parent=self._df, fn=run,
                         step=f"groupBy({', '.join(keys)}).agg({spec})", wide=True)

    def count(self):
        return self.agg({self._keys[0]: "count"})


class DataFrame:
    def __init__(self, session, parts=None, parent=None, fn=None, step="", wide=False):
        self._session = session
        self._parts = parts
        self._parent = parent
        self._fn = fn
        self._step = step
        self._wide = wide

    def _run(self):
        if self._parts is not None:
            return self._parts
        parts = self._fn(self._parent._run())
        self._session.sparkContext.stats.partitions_computed += len(parts)
        return parts

    def _each(self, f, step):
        return DataFrame(self._session, parent=self, fn=lambda parts: [f(p) for p in parts], step=step)

    # ---- transformations (lazy) ---------------------------------------
    def filter(self, condition):
        return self._each(lambda p: p.query(condition), f"filter({condition})")

    where = filter

    def select(self, *cols):
        return self._each(lambda p: p[list(cols)], f"select({', '.join(cols)})")

    def withColumn(self, name, expression):
        return self._each(lambda p: p.assign(**{name: p.eval(expression)}),
                          f"withColumn({name} = {expression})")

    def groupBy(self, *keys):
        return GroupedData(self, list(keys))

    def orderBy(self, col, ascending=True):
        def run(parts):
            whole = pd.concat(parts, ignore_index=True)
            return [whole.sort_values(col, ascending=ascending, kind="stable").reset_index(drop=True)]
        return DataFrame(self._session, parent=self, fn=run, step=f"orderBy({col})", wide=True)

    def limit(self, n):
        def run(parts):
            whole = pd.concat(parts, ignore_index=True)
            return [whole.head(n)]
        return DataFrame(self._session, parent=self, fn=run, step=f"limit({n})")

    # ---- actions --------------------------------------------------------
    def toPandas(self):
        self._session.sparkContext.stats.jobs += 1
        return pd.concat(self._run(), ignore_index=True)

    def count(self):
        self._session.sparkContext.stats.jobs += 1
        return sum(len(p) for p in self._run())

    def collect(self):
        return list(self.toPandas().itertuples(index=False, name=None))

    def show(self, n=20):
        print(self.toPandas().head(n).to_string(index=False))

    @property
    def columns(self):
        return list(self.toPandas().columns)

    def rdd_partitions(self):
        return len(self._run())

    def createOrReplaceTempView(self, name):
        self._session._views[name] = self

    def explain(self):
        steps = []
        df = self
        while df is not None:
            mark = " (shuffle)" if df._wide else ""
            steps.append((df._step or "scan") + mark)
            df = df._parent
        for depth, step in enumerate(steps):
            print("  " * depth + "+- " + step)


class _Builder:
    def appName(self, name):
        return self

    def master(self, url):
        return self

    def getOrCreate(self):
        return SparkSession()


class SparkSession:
    builder = _Builder()

    def __init__(self):
        self.sparkContext = SparkContext()
        self._views = {}

    def createDataFrame(self, data, numPartitions=4):
        frame = data if isinstance(data, pd.DataFrame) else pd.DataFrame(data)
        size = len(frame)
        parts = [frame.iloc[size * i // numPartitions:size * (i + 1) // numPartitions].reset_index(drop=True)
                 for i in range(numPartitions)]
        return DataFrame(self, parts=parts, step=f"createDataFrame({numPartitions} partitions)")

    def sql(self, query):
        con = duckdb.connect()
        for name, df in self._views.items():
            con.register(name, df.toPandas())
        result = con.sql(query).df()
        con.close()
        return self.createDataFrame(result, numPartitions=1)
