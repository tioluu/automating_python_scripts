import boto3
import logging

# Configure logging
logging.basicConfig(
    filename='cleanup.log',
    filemode='w',  # Overwrite the log file for each run
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.info("Cleanup Script Started.")

def cleanup_resources(instance_id, security_group_id, bucket_name, log_group_name):
    ec2_client = boto3.client('ec2', region_name='us-east-1')
    s3_client = boto3.client('s3', region_name='us-east-1')
    logs_client = boto3.client('logs', region_name='us-east-1')

    try:
        # Step 1: Terminate EC2 instance
        logging.info(f"Terminating EC2 instance {instance_id}...")
        ec2_client.terminate_instances(InstanceIds=[instance_id])
        ec2_client.get_waiter('instance_terminated').wait(InstanceIds=[instance_id])
        logging.info(f"Instance {instance_id} terminated.")

        # Step 2: Delete security group
        logging.info(f"Deleting security group {security_group_id}...")
        ec2_client.delete_security_group(GroupId=security_group_id)
        logging.info(f"Security group {security_group_id} deleted.")

        # Step 3: Delete S3 bucket and contents
        logging.info(f"Deleting S3 bucket {bucket_name}...")
        objects = s3_client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in objects:
            for obj in objects['Contents']:
                s3_client.delete_object(Bucket=bucket_name, Key=obj['Key'])
        # Check for versioned objects
        versioning = s3_client.get_bucket_versioning(Bucket=bucket_name)
        if versioning.get('Status') == 'Enabled':
            versions = s3_client.list_object_versions(Bucket=bucket_name)
            if 'Versions' in versions:
                for version in versions['Versions']:
                    s3_client.delete_object(
                        Bucket=bucket_name,
                        Key=version['Key'],
                        VersionId=version['VersionId']
                    )
        s3_client.delete_bucket(Bucket=bucket_name)
        logging.info(f"S3 bucket {bucket_name} deleted.")

        # Step 4: Delete CloudWatch log group
        logging.info(f"Deleting CloudWatch log group {log_group_name}...")
        logs_client.delete_log_group(logGroupName=log_group_name)
        logging.info(f"CloudWatch log group {log_group_name} deleted.")

    except Exception as e:
        logging.error(f"Error during cleanup: {e}")
        raise  # Re-raise the exception for visibility in the main block

if __name__ == "__main__":
    try:
        cleanup_resources(
            instance_id="YOUR_INSTANCE_ID",  # Replace with your instance ID
            security_group_id="YOUR_SECURITY_GROUP_ID",  # Replace with your Security Group ID
            bucket_name="my-devops-ec2-bucket",  # Replace with your bucket name
            log_group_name="/ec2/apache"  # Replace with your CloudWatch log group name
        )
        logging.info("Cleanup complete.")
    except Exception as e:
        logging.error(f"Error in cleanup process: {e}")
