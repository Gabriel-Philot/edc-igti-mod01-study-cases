# import boto3
# import pandas as pd

# s3_client = boto3.client('s3')
                         
# # s3_client.download_file("datalake-gabrielphilot-igti0-4156-5886-9338", "raw-data/microdados_sobe.csv", 'microdados_enem_baixados.csv')

# # df = pd.read_csv("mod_01/microdados_sobe.csv")
# # s3 = boto3.resource('s3')
# # for bucket in s3.buckets.all():
# #     print(bucket.name)
#
# # df = pd.read_csv('microdados_enem_baixados.csv', sep =";" , encoding='latin1')
# # print(df.head())
# s3_client.upload_file("microdados_enem_baixados.csv", "datalake-gabrielphilot-igti0-4156-5886-9338", 'raw-data/microdados_enem.csv')