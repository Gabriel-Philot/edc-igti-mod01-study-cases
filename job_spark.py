# caomentario para notificiar o arquivo .py
import pyspark
from pyspark.sql.functions import mean, max, min, col, count
from pyspark.sql import SparkSession

spark = (
          SparkSession.builder
                      .appName('tarn-csv-to-parquet')
                      .getOrCreate()
         )


enem = (
    spark
    .read
    .format("csv")
    .option("header", True)
    .option("sep", ";")
    .option("encoding", "ISO-8859-1")
    .option("inferSchema", True)
    .load("s3://datalake-gabrielphilot-igti0-4156-5886-9338/raw-data/microdados_enem.csv")
)

(
    enem
    .write
    .mode("overwrite")
    .format("parquet")
    .save("s3://datalake-gabrielphilot-igti0-4156-5886-9338/consumer-zone/microdados_enem")
)

