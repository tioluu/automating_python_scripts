import boto3
import logging

# Configure logging
logging.basicConfig(
    filename='automation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.info("EC2 Automation Script Started.")

# Initialize AWS clients
ec2_client = boto3.client('ec2', region_name='us-east-1')
s3_client = boto3.client('s3', region_name='us-east-1')
cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')

# User data script for EC2 instance
user_data_script = """#!/bin/bash
sudo yum update -y
sudo yum install -y httpd
sudo systemctl start httpd
sudo systemctl enable httpd
echo '<h1>Welcome to My Automated EC2 Instance!</h1>' | sudo tee /var/www/html/index.html
"""

def create_security_group(group_name, description):
    logging.info(f"Creating security group: {group_name}")
    response = ec2_client.create_security_group(
        GroupName=group_name,
        Description=description
    )
    security_group_id = response['GroupId']
    logging.info(f"Security group {group_name} created with ID: {security_group_id}")
    
    # Add inbound rules for SSH and HTTP
    logging.info(f"Adding inbound rules to security group {security_group_id}...")
    ec2_client.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {
                'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]  # Allow SSH from anywhere (for demo purposes)
            },
            {
                'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]  # Allow HTTP from anywhere
            }
        ]
    )
    logging.info(f"Inbound rules added to security group {security_group_id}.")
    return security_group_id

def create_s3_bucket(bucket_name):
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

def create_ec2_instance(security_group_id):
    logging.info("Creating EC2 instance...")
    response = ec2_client.run_instances(
        ImageId="ami-04b4f1a9cf54c11d0",  # Ubuntu
        InstanceType="t2.micro",
        KeyName="newTolu",
        MinCount=1,
        MaxCount=1,
        SecurityGroupIds=[security_group_id],
        Monitoring={'Enabled': True},
        UserData=user_data_script,
    )
    instance_id = response['Instances'][0]['InstanceId']
    logging.info(f"EC2 instance created with ID: {instance_id}")
    return instance_id

def create_cloudwatch_alarm(instance_id):
    logging.info(f"Creating CloudWatch alarm for instance {instance_id}...")
    cloudwatch.put_metric_alarm(
        AlarmName='HighCPUUtilization',
        MetricName='CPUUtilization',
        Namespace='AWS/EC2',
        Statistic='Average',
        Period=300,
        Threshold=80.0,
        ComparisonOperator='GreaterThanThreshold',
        EvaluationPeriods=1,
        AlarmActions=[],  # Add SNS Topic ARN here for notifications
        Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}]
    )
    logging.info("CloudWatch alarm created.")

if __name__ == "__main__":
    try:
        # Step 1: Create a security group
        security_group_name = "EC2_Automation_SG"
        security_group_id = create_security_group(
            group_name=security_group_name,
            description="Security group for EC2 automation script"
        )

        # Step 2: Create an S3 bucket
        bucket_name = "my-devops-ec2-bucket"
        create_s3_bucket(bucket_name)
        upload_file_to_s3(bucket_name, "automation.log")

        # Step 3: Launch EC2 instance
        instance_id = create_ec2_instance(security_group_id)
        logging.info("Waiting for instance to initialize...")
        ec2_client.get_waiter('instance-running').wait(InstanceIds=[instance_id])

        # Step 4: Set up CloudWatch monitoring
        create_cloudwatch_alarm(instance_id)

        logging.info("EC2 automation complete.")

    except Exception as e:
        logging.error(f"Error in automation: {e}")
