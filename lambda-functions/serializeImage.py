import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        bucket = event["s3_bucket"]
        key = event["s3_key"]

        local_path = "/tmp/image.png"
        s3.download_file(bucket, key, local_path)

        with open(local_path, "rb") as f:
            image_data = f.read()

        base64_image = base64.b64encode(image_data).decode("utf-8")

        print(f"Original image size: {len(image_data)} bytes")
        print(f"Base64 encoded image length: {len(base64_image)}")

        return {
            'statusCode': 200,
            'body': {
                "image_data": base64_image,
                "s3_bucket": bucket,
                "s3_key": key,
                "inferences": []
            }
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'error': str(e)
        }
