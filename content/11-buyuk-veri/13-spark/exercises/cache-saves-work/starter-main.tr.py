from minispark import SparkSession

spark = SparkSession.builder.appName("orders").getOrCreate()
sc = spark.sparkContext

nums = sc.parallelize(range(1_000), 4)

# Onbelleksiz: iki eylem ve sayactaki artis.


# Onbellekli: iki eylem ve sayactaki artis.


# Iki toplam ayni mi?
