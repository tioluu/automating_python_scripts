import boto3
import logging

def create_cloudwatch_alarm(instance_id):
    cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
    
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