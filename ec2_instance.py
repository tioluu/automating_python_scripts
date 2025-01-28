import boto3
import logging


def create_ec2_instance(security_group_id):
    ec2_client = boto3.client('ec2', region_name='us-east-1')
    
    # Read the user data script from the file
    with open('user_data.sh', 'r') as file:
        user_data_script = file.read()
    
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