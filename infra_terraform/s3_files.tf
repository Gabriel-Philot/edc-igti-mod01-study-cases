

# File spark job for emr
resource "aws_s3_object" "codigo_spark_emr" {
  bucket = aws_s3_bucket.datalake.id #Referêrncia do datalake criado
  key    = "emr-code/pyspark/delta_spark_01_insert.py"
  source = "../etl/delta_spark_01_insert.py"          # Arquivo com o job spark que vai
  etag   = filemd5("../etl/delta_spark_01_insert.py") # Define qual é o objeto de parâmetro
}

# File spark job for glue
resource "aws_s3_object" "codigo_spark_glue" {
  bucket = aws_s3_bucket.datalake.id #Referêrncia do datalake criado
  key    = "glue_job-code/pyspark/delta_spark_uspert_02.py.py"
  source = "../etl/delta_spark_uspert_02.py"          # Arquivo com o job spark que vai
  etag   = filemd5("../etl/delta_spark_uspert_02.py") # Define qual é o objeto de parâmetro
}