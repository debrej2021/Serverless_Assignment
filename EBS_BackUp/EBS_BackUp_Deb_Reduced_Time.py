import boto3
from datetime import datetime, timedelta, timezone
from concurrent.futures import ThreadPoolExecutor

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

    # Calculate the cutoff time for snapshots to delete (older than 30 days)
    cutoff_time = datetime.now(timezone.utc) - timedelta(days=30)

    # Filter snapshots older than 30 days
    snapshots_to_delete = [
        snapshot['SnapshotId']
        for snapshot in snapshots
        if snapshot['StartTime'] < cutoff_time
    ]
    
    def delete_snapshot(snapshot_id):
        try:
            # Attempt to delete the snapshot
            ec2.delete_snapshot(SnapshotId=snapshot_id)
            print(f"Deleted snapshot ID: {snapshot_id}")
        except Exception as e:
            # Catch errors, likely due to snapshot being in use
            print(f"Could not delete snapshot ID: {snapshot_id}, error: {str(e)}")

    # Use ThreadPoolExecutor to delete snapshots in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(delete_snapshot, snapshots_to_delete)
