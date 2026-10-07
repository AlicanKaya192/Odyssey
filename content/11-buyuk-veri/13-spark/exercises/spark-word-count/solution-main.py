from minispark import SparkSession

spark = SparkSession.builder.appName("orders").getOrCreate()
sc = spark.sparkContext

text = [
    "spark keeps data in memory",
    "spark splits data into partitions",
    "data moves in a shuffle",
    "memory makes spark fast",
]

lines = sc.parallelize(text, 2)
counts = (lines.flatMap(lambda line: line.split())
               .map(lambda word: (word, 1))
               .reduceByKey(lambda a, b: a + b)
               .sortBy(lambda kv: (-kv[1], kv[0])))

for word, count in counts.take(4):
    print(word, count)
print(counts.count())
