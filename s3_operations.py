import boto3
import logging

s3_client = boto3.client('s3', region_name='us-east-1')

def create_s3_bucket(bucket_name):
    logging.info(f"Creating S3 bucket: {bucket_name}")
    try:
        # No CreateBucketConfiguration for us-east-1
        s3_client.create_bucket(Bucket=bucket_name)
        logging.info(f"S3 bucket {bucket_name} created.")
    except Exception as e:
        logging.error(f"Error creating bucket {bucket_name}: {e}")
        raise
    return bucket_name

def upload_file_to_s3(bucket_name, file_name, object_name=None):
    logging.info(f"Uploading {file_name} to S3 bucket {bucket_name}...")
    object_name = object_name or file_name
    try:
        s3_client.upload_file(file_name, bucket_name, object_name)
        logging.info(f"{file_name} uploaded to {bucket_name} as {object_name}.")
    except Exception as e:
        logging.error(f"Error uploading {file_name} to {bucket_name}: {e}")
        raise
