import boto3
from datetime import datetime, timezone

def lambda_handler(event, context):
    # Initialize a Boto3 S3 client
    s3 = boto3.client('s3')

    # Specify the bucket name
    bucket_name = 's3clearlambdadeb'

    # List objects in the specified bucket
    try:
        # Fetch the objects in the bucket
        objects = s3.list_objects_v2(Bucket=bucket_name)

        # Get the current date and time
        current_time = datetime.now(timezone.utc)

        # Check if there are any objects in the bucket
        if 'Contents' in objects:
            for obj in objects['Contents']:
                # Get the object's last modified date
                last_modified_date = obj['LastModified']
                
                # Debug: Print the last modified date
                print(f"Object: {obj['Key']}, LastModified: {last_modified_date}")

                # Calculate the age of the object
                object_age = (current_time - last_modified_date).days

                # Debug: Print the calculated age
                print(f"Object: {obj['Key']}, Age: {object_age} days")

                # Delete the object if it's older than 30 days
                if object_age > 30:
                    s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
                    print(f"Deleted object: {obj['Key']}")
                else:
                    print(f"Object {obj['Key']} is not older than 30 days.")

        return {
            'statusCode': 200,
            'body': 'Old objects deletion check completed successfully!'
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }
