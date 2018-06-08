import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # TODO implement
    
    client = boto3.client('ec2')
    ec2 = boto3.resource('ec2')
    
    response = client.describe_snapshots(OwnerIds=['self'])
    
    if response:
    
        for snapshot in response['Snapshots']:
            SnapshotId = snapshot['SnapshotId']
            volumeId = snapshot['VolumeId']
            
            snapshot_obj = ec2.Snapshot(SnapshotId)
            volume_obj = ec2.Volume(volumeId)
        
            print(volume_obj.tags)
            
            if volume_obj.tags:
                snapshot_obj.create_tags(Tags=volume_obj.tags)
                logger.info("Volume Id : {} and Snapshot Id : {}".format(volumeId,SnapshotId))
            else:
                logger.info("Volume does not have the tags")
            
    else:
        logger.info('No Snapshots observed in the region')
       
    return True
