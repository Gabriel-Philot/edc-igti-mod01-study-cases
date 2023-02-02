import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# A partir daqui, exatamente o mesmo codigo executado no EMR

# Ler dados do enem 2020

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

# Escrita dos dados no formato parquet

(
enem
.write
.mode("overwrite")
.format("parquet")
.save("s3://datalake-gabrielphilot-igti0-4156-5886-9338/consumer-zone/microdados_enem-glue")
)

job.commit()