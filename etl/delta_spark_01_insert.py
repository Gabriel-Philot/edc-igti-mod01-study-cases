
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, min, max

# Cria objeto da Spark Session
spark = (SparkSession.builder.appName("Lambdaemrex")
    .getOrCreate()
)


# Leitura de dados
enem = (
    spark
    .read
    .format("csv")
    .option("header", True)
    .option("sep", ";")
    .option("encoding", "ISO-8859-1")
    .option("inferSchema", True)
    .load("s3://datalake-edc-mod1-studycases-prod/raw-data/microdados_sobe.csv")
)

# Escreve a tabela em staging em formato delta
print("Writing delta table...")
(
    enem
    .write
    .mode("overwrite")
    .format("parquet")
    .save("datalake-edc-mod1-studycases-prod/staging-zone/")
)