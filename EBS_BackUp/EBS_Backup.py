import boto3
from datetime import datetime, timedelta, timezone

def lambda_handler(event, context):
    # Initialize EC2 client
    ec2 = boto3.client('ec2')

    # Your EBS volume ID
    volume_id = 'vol-0fbfb7bed736663df'

    # Create a snapshot
    snapshot = ec2.create_snapshot(VolumeId=volume_id, Description='Automated snapshot by Lambda')
    print(f"Created snapshot ID: {snapshot['SnapshotId']}")

    # List snapshots
    snapshots = ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']
    print(f"Found {len(snapshots)} snapshots")

    # Delete snapshots older than 30 days
    for snapshot in snapshots:
        # Make datetime.now() timezone-aware
        if snapshot['StartTime'] < datetime.now(timezone.utc) - timedelta(days=30):
            try:
                # Attempt to delete the snapshot
                ec2.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
                print(f"Deleted snapshot ID: {snapshot['SnapshotId']}")
            except Exception as e:
                # Catch errors, likely due to snapshot being in use
                print(f"Could not delete snapshot ID: {snapshot['SnapshotId']}, error: {str(e)}")
