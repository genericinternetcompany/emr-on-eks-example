# emr-on-eks-example

## Example Prerequisites

* Setup Virtual Cluster: [here](https://docs.aws.amazon.com/emr/latest/EMR-on-EKS-DevelopmentGuide/setting-up.html)
* S3 Bucket

## Execution Steps
* Update test-processor.py for your bucket by replacing the paths in "sqlDF.write.parquet"
* Place test-processor.py in s3 bucket that cluster role can access.
* Update Virtual Cluster ID, Execution arn and entrypoint for your environment
* open console with aws cli configured and pointing to project folder and run: aws emr-containers start-job-run --cli-input-json file://./emr-eks.json

### Solution only works on 2xlarge instance types or better.

