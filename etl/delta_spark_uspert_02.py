import logging
import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, min, max, lit

# Configuracao de logs de aplicacao#
logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger('datalake_enem_small_upsert')
logger.setLevel(logging.DEBUG)

# Definicao da Spark Session
spark = (SparkSession.builder.appName("DeltaExercise")
    .config("spark.jars.packages", "io.delta:delta-core_2.12:1.0.0")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .getOrCreate()
)


logger.info("Importing delta.tables...")
from delta.tables import *


logger.info("Produzindo novos dados...")
enemnovo = (
    spark.read.format("delta")
    .load("datalake-edc-mod1-studycases-prod/staging-zone/enem")
)

# Define algumas inscricoes (chaves) que serao alteradas
inscricoes = [200003934219, 200002355621, 200002834896, 200002586687, 200002653960, 200005566429, 200002647665, 200001488217, 200001069725, 200003709574, 200003424512, 200006376754, 200001106035, 200004625950, 200005954932, 200001551006, 200001154299, 200006580985, 200001948547, 200003597858, 200002103865, 200001815781, 200004345289, 200006081355, 200002607253, 200002299983, 200002031020, 200004724167, 200005181125, 200003066067]

logger.info("Reduz a 50 casos e faz updates internos no municipio de residencia")
enemnovo = enemnovo.where(enemnovo.NU_INSCRICAO.isin(inscricoes))
enemnovo = enemnovo.withColumn("NO_MUNICIPIO_RESIDENCIA", lit("NOVA CIDADE")).withColumn("CO_MUNICIPIO_RESIDENCIA", lit(10000000))


logger.info("Pega os dados do Enem velhos na tabela Delta...")
enemvelho = DeltaTable.forPath(spark, "datalake-edc-mod1-studycases-prod/staging-zone/enem")


logger.info("Realiza o UPSERT...")
(
    enemvelho.alias("old")
    .merge(enemnovo.alias("new"), "old.NU_INSCRICAO = new.NU_INSCRICAO")
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute()
)

logger.info("Atualizacao completa! \n\n")

logger.info("Gera manifesto symlink...")
enemvelho.generate("symlink_format_manifest")

logger.info("Manifesto gerado.")