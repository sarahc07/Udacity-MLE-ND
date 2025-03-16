import json

THRESHOLD = 0.9  

def lambda_handler(event, context):
    """Filter out low-confidence inferences"""

    print("Received event:", json.dumps(event))

    inferences = event.get("inferences", [])

    print("Extracted inferences:", inferences)

    meets_threshold = any(x > THRESHOLD for x in inferences)

    if meets_threshold:
        return {
            'statusCode': 200,
            'body': json.dumps(event)
        }
    
    else:
        raise Exception("THRESHOLD_CONFIDENCE_NOT_MET")
