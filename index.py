import json
import boto3
import os

dynamodb = boto3.client('dynamodb')
table_name = os.environ['TABLE_NAME']

def handler(event, context):
    try:
        # Extract object details from the event
        s3_event = event.get("detail", {})
        bucket_name = s3_event.get("requestParameters", {}).get("bucketName")
        object_key = s3_event.get("requestParameters", {}).get("key")

        if not bucket_name or not object_key:
            raise ValueError("Invalid event format")

        visit_id = "visit_count"

        # Increment count atomically
        response = dynamodb.update_item(
            TableName=table_name,
            Key={"id": {"S": visit_id}},
            UpdateExpression="ADD #count :inc",
            ExpressionAttributeNames={"#count": "count"},
            ExpressionAttributeValues={":inc": {"N": "1"}},
            ReturnValues="UPDATED_NEW"
        )

        new_count = response["Attributes"]["count"]["N"]
        print(f"Updated visit count: {new_count}")
        print("made few changes using the github actions")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Visit count updated successfully',
                'count': new_count
            })
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error updating visit count', 'error': str(e)})
        }
