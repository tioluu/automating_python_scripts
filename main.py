import boto3
import logging
from security_group import create_security_group
from s3_operations import create_s3_bucket, upload_file_to_s3
from ec2_instance import create_ec2_instance
from cloudwatch_alarm import create_cloudwatch_alarm

# Configure logging
logging.basicConfig(
    filename='automation.log',
    filemode='w',  # Overwrite the log file for each run
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.info("EC2 Automation Script Started.")

if __name__ == "__main__":
    try:
        # Step 1: Create a security group
        security_group_id = create_security_group()

        # Step 2: Create an S3 bucket
        bucket_name = "my-devops-ec2-bucket"
        create_s3_bucket(bucket_name)
        upload_file_to_s3(bucket_name, "automation.log")

        # Step 3: Launch EC2 instance
        instance_id = create_ec2_instance(security_group_id)
        logging.info("Waiting for instance to initialize...")
        ec2_client = boto3.client('ec2', region_name='us-east-1')
        ec2_client.get_waiter('instance_running').wait(InstanceIds=[instance_id])

        # Step 4: Set up CloudWatch monitoring
        create_cloudwatch_alarm(instance_id)

        logging.info("EC2 automation complete.")

    except Exception as e:
        logging.error(f"Error in automation: {e}")
