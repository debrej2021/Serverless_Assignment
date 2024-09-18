import boto3

def lambda_handler(event, context):
    # Initialize EC2 client
    ec2 = boto3.client('ec2')

    # Stop instances with the 'Auto-Stop' tag
    auto_stop_instances = ec2.describe_instances(
        Filters=[
            {'Name': 'tag:Name1', 'Values': ['Deb-Auto-Stop']},
            {'Name': 'instance-state-name', 'Values': ['running']}
        ]
    )

    for reservation in auto_stop_instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            print(f"Stopping instance: {instance_id}")
            ec2.stop_instances(InstanceIds=[instance_id])

    # Start instances with the 'Auto-Start' tag
    auto_start_instances = ec2.describe_instances(
        Filters=[
            {'Name': 'tag:Name1', 'Values': ['Deb-Auto-Start']},
            {'Name': 'instance-state-name', 'Values': ['stopped']}
        ]
    )

    for reservation in auto_start_instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            print(f"Starting instance: {instance_id}")
            ec2.start_instances(InstanceIds=[instance_id])

    return {
        'statusCode': 200,
        'body': 'Auto-start and auto-stop operations completed successfully!'
    }
