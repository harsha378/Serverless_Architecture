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