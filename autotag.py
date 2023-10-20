import boto3
import datetime

def lambda_handler(event, context):
    # Initialize an EC2 client
    ec2 = boto3.client('ec2')
    
    # Retrieve the instance ID from the event
    instance_id = event['detail']['responseElements']['instancesSet']['items'][0]['instanceId']
    
    # Tag the new instance with the current date and another custom tag
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    custom_tag = "Very Good"
    
    ec2.create_tags(Resources=[instance_id], Tags=[{'Key': 'LaunchDate', 'Value': current_date}, {'Key': 'CustomTag', 'Value': custom_tag}])
    
    # Print a confirmation message for logging purposes
    print(f"Instance {instance_id} has been tagged with LaunchDate: {current_date} and CustomTag: {custom_tag}")
