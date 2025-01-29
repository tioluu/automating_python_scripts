import boto3
import logging

# Configure logging
logging.basicConfig(
    filename='cleanup.log',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.info("Cleanup Script Started.")

def get_instance_details():
    """Fetch instance and security group details dynamically."""
    ec2_client = boto3.client('ec2', region_name='us-east-1')
    response = ec2_client.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    
    if not response['Reservations']:
        logging.info("No running EC2 instances found. Skipping instance termination.")
        return None, None  # No instance found

    instance = response['Reservations'][0]['Instances'][0]
    instance_id = instance['InstanceId']
    security_group_id = instance['SecurityGroups'][0]['GroupId']
    
    return instance_id, security_group_id

def delete_s3_bucket(bucket_name):
    """Deletes all objects, versions, and the bucket itself."""
    s3_client = boto3.client('s3', region_name='us-east-1')

    try:
        # Check if the bucket exists
        s3_client.head_bucket(Bucket=bucket_name)
        logging.info(f"Deleting all objects from S3 bucket {bucket_name}...")

        # Delete all objects
        objects = s3_client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in objects:
            for obj in objects['Contents']:
                s3_client.delete_object(Bucket=bucket_name, Key=obj['Key'])

        # Delete all object versions if bucket versioning is enabled
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
            if 'DeleteMarkers' in versions:
                for marker in versions['DeleteMarkers']:
                    s3_client.delete_object(
                        Bucket=bucket_name,
                        Key=marker['Key'],
                        VersionId=marker['VersionId']
                    )

        # Delete the bucket
        logging.info(f"Deleting S3 bucket {bucket_name}...")
        s3_client.delete_bucket(Bucket=bucket_name)
        logging.info(f"S3 bucket {bucket_name} deleted.")

    except s3_client.exceptions.NoSuchBucket:
        logging.info(f"S3 bucket {bucket_name} does not exist. Skipping bucket deletion.")
    except Exception as e:
        logging.error(f"Error deleting S3 bucket {bucket_name}: {e}")

def delete_cloudwatch_alarm(alarm_name):
    """Deletes the CloudWatch alarm."""
    cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')

    try:
        # Check if the alarm exists
        cloudwatch.describe_alarms(AlarmNames=[alarm_name])
        logging.info(f"Deleting CloudWatch alarm {alarm_name}...")
        cloudwatch.delete_alarms(AlarmNames=[alarm_name])
        logging.info(f"CloudWatch alarm {alarm_name} deleted.")
    except cloudwatch.exceptions.ResourceNotFoundException:
        logging.info(f"CloudWatch alarm {alarm_name} does not exist. Skipping alarm deletion.")
    except Exception as e:
        logging.error(f"Error deleting CloudWatch alarm {alarm_name}: {e}")

def cleanup_resources(instance_id, security_group_id, bucket_name, log_group_name, alarm_name):
    ec2_client = boto3.client('ec2', region_name='us-east-1')
    logs_client = boto3.client('logs', region_name='us-east-1')

    try:
        # Step 1: Terminate EC2 instance (if found)
        if instance_id:
            logging.info(f"Terminating EC2 instance {instance_id}...")
            ec2_client.terminate_instances(InstanceIds=[instance_id])
            ec2_client.get_waiter('instance_terminated').wait(InstanceIds=[instance_id])
            logging.info(f"Instance {instance_id} terminated.")
        else:
            logging.info("No EC2 instance to terminate. Skipping instance cleanup.")

        # Step 2: Delete security group (if found)
        if security_group_id:
            logging.info(f"Deleting security group {security_group_id}...")
            ec2_client.delete_security_group(GroupId=security_group_id)
            logging.info(f"Security group {security_group_id} deleted.")
        else:
            logging.info("No security group to delete. Skipping security group cleanup.")

        # Step 3: Delete S3 bucket and contents
        delete_s3_bucket(bucket_name)

        # Step 4: Delete CloudWatch log group
        try:
            logs_client.describe_log_groups(logGroupNamePrefix=log_group_name)
            logging.info(f"Deleting CloudWatch log group {log_group_name}...")
            logs_client.delete_log_group(logGroupName=log_group_name)
            logging.info(f"CloudWatch log group {log_group_name} deleted.")
        except logs_client.exceptions.ResourceNotFoundException:
            logging.info(f"CloudWatch log group {log_group_name} does not exist. Skipping log group deletion.")

        # Step 5: Delete CloudWatch alarm
        delete_cloudwatch_alarm(alarm_name)

    except Exception as e:
        logging.error(f"Error during cleanup: {e}")

if __name__ == "__main__":
    try:
        instance_id, security_group_id = get_instance_details()  # Fetch instance & SG dynamically
        alarm_name = "HighCPUUtilization"  # Replace with your CloudWatch alarm name
        cleanup_resources(
            instance_id=instance_id,
            security_group_id=security_group_id,
            bucket_name="my-devops-ec2-bucket",  # Replace with your bucket name
            log_group_name="/ec2/apache",  # Replace with your CloudWatch log group name
            alarm_name=alarm_name
        )
        logging.info("Cleanup complete.")
    except Exception as e:
        logging.error(f"Error in cleanup process: {e}")
