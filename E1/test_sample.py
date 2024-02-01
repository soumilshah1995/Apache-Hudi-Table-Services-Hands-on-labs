"""
%connections aurora.jtedw.landing
%idle_timeout 2880
%glue_version 4.0
%worker_type G.1X
%number_of_workers 5
"""

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)


glue_df = glueContext.create_sample_dynamic_frame_from_catalog(
    database="pgm.dynamodb.prod",
    table_name="table_name_pgm_employer_context_job",
    transformation_ctx="AWSGlueDagreat taCatalog_node1670851559339",
    num=100
)

glue_df.show()