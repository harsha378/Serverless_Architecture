import boto3
import datetime

def lambda_handler(event, context):
    # Initialize an S3 client
    s3 = boto3.client('s3')

    # Specify the bucket name
    bucket_name = 'harshab'

    # Calculate the date threshold (30 days ago)
    threshold_date = (datetime.datetime.now() - datetime.timedelta(days=30)).date()

    # List objects in the S3 bucket
    objects = s3.list_objects(Bucket=bucket_name)

    # Delete objects older than 30 days
    for obj in objects.get('Contents', []):
        last_modified = obj['LastModified'].date()
        if last_modified < threshold_date:
            s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
            print(f"Deleted object: {obj['Key']}")