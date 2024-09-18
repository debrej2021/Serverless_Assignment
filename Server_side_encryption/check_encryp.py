import boto3

def lambda_handler(event, context):
    # Initialize a boto3 S3 client
    s3_client = boto3.client('s3')

    # List all S3 buckets
    response = s3_client.list_buckets()
    buckets = response['Buckets']

    # List to store unencrypted buckets
    unencrypted_buckets = []

    for bucket in buckets:
        bucket_name = bucket['Name']
        try:
            # Check for bucket encryption
            encryption = s3_client.get_bucket_encryption(Bucket=bucket_name)
            rules = encryption['ServerSideEncryptionConfiguration']['Rules']
            # If rules are present, bucket has some encryption settings
            if not rules:
                # No encryption rules found, consider this bucket unencrypted
                unencrypted_buckets.append(bucket_name)
        except s3_client.exceptions.ClientError as e:
            # Check if the error is because encryption is not configured
            error_code = e.response['Error']['Code']
            if error_code == 'ServerSideEncryptionConfigurationNotFoundError':
                # Bucket has no default server-side encryption
                unencrypted_buckets.append(bucket_name)
            else:
                # Log any other errors (e.g., access denied)
                print(f"Error checking encryption for bucket {bucket_name}: {e}")

    # Print the names of unencrypted buckets for logging purposes
    if unencrypted_buckets:
        print("Buckets without default server-side encryption:")
        for unencrypted_bucket in unencrypted_buckets:
            print(unencrypted_bucket)
    else:
        print("All buckets are encrypted by default.")
    
    # Return the result for logging or further processing
    return {
        'unencrypted_buckets': unencrypted_buckets,
        'message': 'Check the logs for details'
    }
