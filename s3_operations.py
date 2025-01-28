import boto3
import logging

def create_s3_bucket(bucket_name):
    s3_client = boto3.client('s3', region_name='us-east-1')
    
    logging.info(f"Creating S3 bucket: {bucket_name}")
    s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
        'LocationConstraint': 'us-east-1'
    })
    logging.info(f"S3 bucket {bucket_name} created.")
    return bucket_name

def upload_file_to_s3(bucket_name, file_name, object_name=None):
    logging.info(f"Uploading {file_name} to S3 bucket {bucket_name}...")
    object_name = object_name or file_name
    s3_client.upload_file(file_name, bucket_name, object_name)
    logging.info(f"{file_name} uploaded to {bucket_name} as {object_name}.")
    