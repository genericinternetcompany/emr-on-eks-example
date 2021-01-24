#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import StringType
from pyspark import SQLContext
from itertools import islice
from pyspark.sql.functions import col

import sys

if __name__ == '__main__':

    spark = SparkSession\
        .builder\
        .config('spark.sql.debug.maxToStringFields', 2000) \
        .config('spark.debug.maxToStringFields', 2000) \
        .getOrCreate()

    input_bucket = 's3://commoncrawl/cc-index/table/cc-main/warc/crawl=CC-MAIN-2020-45/'
    df = spark.read.parquet(input_bucket)
    df.createOrReplaceTempView("urls")
    sqlDF = spark.sql("""SELECT url_host_tld AS Top_Level_Domain, COUNT(*) AS Number_Of_Pages, COUNT(DISTINCT url_host_name) AS Number_Of_Hosts, COUNT(DISTINCT url_host_registered_domain) AS Number_Of_Domains 
                        FROM urls 
                        GROUP BY url_host_tld
                        ORDER BY Number_Of_Pages DESC""")
    sqlDF.write.parquet('s3://mdigiacomi-emr-testbucket/output/' + spark.sparkContext.applicationId + '/testparquet.parquet')
    sqlDF = spark.sql("""SELECT COUNT(*) AS count, url_host_registered_domain 
                        FROM urls 
                        WHERE url_host_tld = 'com'
                        GROUP BY url_host_registered_domain
                        ORDER BY count desc""")
    sqlDF.write.parquet('s3://mdigiacomi-emr-testbucket/output/' + spark.sparkContext.applicationId + '/testparquet2.parquet')
    sqlDF = spark.sql("""SELECT COUNT(*) AS count, url_host_registered_domain
                        FROM urls 
                        WHERE url_host_tld = 'org'
                        GROUP BY url_host_registered_domain
                        ORDER BY count DESC""")
    sqlDF.write.parquet('s3://mdigiacomi-emr-testbucket/output/' + spark.sparkContext.applicationId + '/testparquet3.parquet')
