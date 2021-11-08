from pyspark import SparkConf
from pyspark.context import SparkContext
from pyspark.streaming import StreamingContext


sc = SparkContext.getOrCreate(SparkConf().setMaster("local[*]"))
ssc = StreamingContext(sc, 1)

PORT=20777
HOST="localhost"

lines = ssc.socketTextStream(HOST, PORT)
counts = lines.flatMap(lambda line: line.split(" "))\
              .map(lambda word: (word, 1))\
              .reduceByKey(lambda a, b: a+b)
counts.pprint()

ssc.start()
ssc.awaitTerminationOrTimeout(60) # wait 60 seconds