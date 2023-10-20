import boto3

def lambda_handler(event, context):
    # Initialize an EC2 client
    ec2 = boto3.client('ec2')

    # Describe instances with the 'Auto-Stop' and 'Auto-Start' tags
    auto_stop_instances = ec2.describe_instances(Filters=[{'Name': 'tag:Action', 'Values': ['Auto-Stop']}])
    auto_start_instances = ec2.describe_instances(Filters=[{'Name': 'tag:Action', 'Values': ['Auto-Start']}])

    # Stop 'Auto-Stop' instances
    for reservation in auto_stop_instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            ec2.stop_instances(InstanceIds=[instance_id])
            print(f"Stopped instance: {instance_id}")

    # Start 'Auto-Start' instances
    for reservation in auto_start_instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            ec2.start_instances(InstanceIds=[instance_id])
            print(f"Started instance: {instance_id}")