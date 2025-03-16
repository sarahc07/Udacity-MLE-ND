import json
import boto3
import base64
import os

# Get SageMaker endpoint from environment variables
ENDPOINT = os.environ['ENDPOINT']

def lambda_handler(event, context):
    try:
        # Decode the image data from base64
        image = base64.b64decode(event['body']['image_data'])

        # Create SageMaker runtime client
        runtime = boto3.client('runtime.sagemaker')


        # Make a prediction request with raw binary image data
        response = runtime.invoke_endpoint(
            EndpointName=ENDPOINT,
            ContentType="application/x-image",  # Adjust content type if needed
            Body=image
        )

        inferences = response["Body"].read().decode("utf-8")

        return {
            'statusCode': 200,
            'body': {
                "image_data": event['body']['image_data'],
                "s3_bucket": event['body']['s3_bucket'],
                "s3_key": event['body']['s3_key'],
                "inferences": json.loads(inferences),
            }
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'error': str(e)
        }
