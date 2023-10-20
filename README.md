# Assignment-1

*  Certainly, here are step-by-step instructions to achieve your goal of automating the stopping and starting of EC2 instances based on tags using AWS services and Boto3 in a Lambda function.

* Create two Ec2 instances.

* Tag one instance with a key 'Action' and a value 'Auto-Stop'.

* Tag one instance with a key 'Action' and a value 'Auto-Start'.

# 2. Lambda IAM Role:

* Go to the AWS IAM dashboard.

* Create a new IAM role for the Lambda function. Name it something like EC2-Tag-Based-Automation.

* Attach the AmazonEC2FullAccess policy to this role. 

* Click on "Create function" to create the Lambda function.

* In the Lambda function code editor, write a Python script using Boto3 to automate EC2 instance management based on tags. Here's an example script:


```bash

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
```

* Save the Lambda function code.

## 4. Manual Invocation:

* After saving the Lambda function, you can manually trigger it for testing.

* Go to the Lambda dashboard, select your function, and click the "Test" button.

* Configure a test event (you can use a simple JSON object as a test event, for example, {}).

* Click "Create" to save the test event and then click "Test" to manually invoke the Lambda function.

## 5. Verification:

* Go to the EC2 dashboard to confirm that the instances' states have changed as expected.

* The instance tagged Auto-Stop should be stopped, and the instance tagged Auto-Start should be started.

* Please be cautious when setting up IAM permissions, and in a production environment, follow the principle of least privilege by giving the Lambda function only the necessary permissions to perform the required actions on EC2 instances.

# Assignment 2: 

## Automated S3 Bucket Cleanup Using AWS Lambda and Boto3

* Task: Automate the deletion of files older than 30 days in a specific S3 bucket.


## Instructions:

## S3 Setup:

*  Navigate to the S3 dashboard and create a new bucket.

Create a new S3 bucket or use an existing one.
Upload multiple files to this bucket. Ensure that you have some files that are older than 30 days. You can use old files or adjust the file timestamps temporarily for testing.

## 2. Lambda IAM Role:

Go to the AWS IAM dashboard.
Create a new IAM role for your Lambda function. Name it something like S3-Cleanup-Role.
Attach the AmazonS3FullAccess policy to this role. This policy provides full access to all S3 buckets and objects, which is appropriate for this task. In a production environment, you would use a more restrictive policy.

## 3. Lambda Function:

* Go to the AWS Lambda dashboard.
Click on "Create function" and choose "Author from scratch."

* Configure the function as follows:
Name: Give your Lambda function a name, e.g., S3CleanupFunction.

* Runtime: Choose Python 3.x.
Role: Select the IAM role you created earlier (S3-Cleanup-Role).

* Click on "Create function" to create the Lambda function.

* In the Lambda function code editor, write a Python script using Boto3 to automate the S3 cleanup task. Here's an example script:

```bash
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
```


## 4. Manual Invocation:

* After saving the Lambda function, you can manually trigger it for testing.

* Go to the Lambda dashboard, select your function, and click the "Test" button.

* Configure a test event (you can use a simple JSON object as a test event, for example, {}).

* Click "Create" to save the test event, and then click "Test" to manually invoke the Lambda function.

5. Verification:

* Go to the S3 dashboard to confirm that only files newer than 30 days remain in your S3 bucket. The Lambda function will have deleted files older than 30 days.

* This Lambda function will automatically clean up old files in the specified S3 bucket, making it a useful tool for maintaining data retention policies and managing storage costs.


# Assignment-6


## Step1 EC2 Setup:

* Ensure you have the capability to launch EC2 instances. Make sure you have the necessary permissions to create and manage EC2 instances.

## Step2. Lambda IAM Role:

* In the IAM dashboard, create a new role for Lambda.

* Attach the AmazonEC2FullAccess policy to this role. This policy provides Lambda with the necessary permissions to interact with EC2 instances.

## Step3. Lambda Function:

* Navigate to the Lambda dashboard in the AWS Management Console and create a new function.

* Choose Python 3.x as the runtime.
Assign the IAM role created in the previous step to the Lambda function.

```py
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


```
## Step 4. CloudWatch Events:

* Set up a CloudWatch Event Rule to trigger the Lambda function when a new EC2 instance is launched:

* Go to the CloudWatch dashboard.
Under "Events," click "Rules" and then "Create rule."
* Choose "Event Source" as "Event Source Type: EC2 Instance State-change Notification."
* Select "Specific state(s)" and choose "running."

* Under "Targets," click "Add target," and select your Lambda function from the dropdown.

* Click "Configure details" and name your rule.
Click "Create rule."

## Step5. Testing:

* To test the setup, launch a new EC2 instance. After a short delay, the instance should be automatically tagged with the current date and our custom tag.

## Assignment 9 Analyze Sentiment of User Reviews Using AWS Lambda, Boto3, and Amazon Comprehend


## Step 1: Create an IAM Role for Lambda

* Go to the AWS IAM dashboard.

* Click on "Roles" and then "Create Role."

* Choose "AWS Lambda" as the use case and click "Next: Permissions."

* Search for and attach policies that      allow Lambda to use Amazon Comprehend. You might want to use policies like "ComprehendFullAccess" to grant the necessary permissions.

* Review and name the role, then create it.


## Step 2: Create a Lambda Function

Go to the AWS Lambda dashboard.

* Click on "Create function."

* Choose "Author from scratch," and configure the following:

* Name: Give your Lambda function a name.
Runtime: Choose "Python 3.x."

* Execution role: Choose "Use an existing role" and select the IAM role you created in Step 1.

* Click "Create function" to create the Lambda function.

## Step 3: Write the Boto3 Python Script

```py
import boto3
import json
import logging

# Initialize the Comprehend client
comprehend = boto3.client('comprehend')

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        # Extract the user review from the Lambda event
        user_review = event['user_review']
        
        # Use Amazon Comprehend to analyze the sentiment
        sentiment_response = comprehend.detect_sentiment(Text=user_review, LanguageCode='en')
        sentiment = sentiment_response['Sentiment']
        
        # Log the sentiment result
        logger.info(f"Sentiment analysis result for the review: {user_review}")
        logger.info(f"Sentiment: {sentiment}")

        return {
            'statusCode': 200,
            'body': json.dumps(sentiment)
        }

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error occurred while analyzing sentiment.')
        }

```

* We import the necessary libraries, initialize the Comprehend client, and set up logging.

* In the lambda_handler function, we extract the user review from the Lambda event, use Amazon Comprehend to analyze the sentiment, log the sentiment result, and return the result as a JSON response.

## Step 4: Testing

* To test your Lambda function:

* Manually trigger the Lambda function from the AWS Lambda dashboard by configuring a test event with a sample user review.

* After triggering the function, check the CloudWatch Logs associated with the Lambda function to confirm the sentiment analysis results.

* That's it! You've successfully set up a Lambda function to analyze the sentiment of user reviews using AWS Lambda, Boto3, and Amazon Comprehend.

```json
{
  "user_review": "This is a sample user review. The product is awesome!"
}
```

* Please specify the json object in the test configuration


# THE END



