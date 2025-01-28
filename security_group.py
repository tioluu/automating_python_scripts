import boto3
import logging

def create_security_group():
    group_name = 'EC2_Automation_SG'
    description = 'Security group for EC2 automation script'
    
    ec2_client = boto3.client('ec2', region_name='us-east-1')
    
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
