import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


ec2 = boto3.resource('ec2')

def instance_volume_tags_creator(event, context):
    # TODO implement
    
    for i in ec2.instances.all():
        
        #print instance id
        logger.info("Instance Id {}".format(i.id))
        
        instance = ec2.Instance(i.id)
        
        instance_tags = instance.tags
        
        #check instance tags whether these are empty or not?
        
        if instance_tags:
        
            logger.info ("{} : available tags are {}".format(i.id,instance_tags))
            
            # get volumes for the specified instances
            volumes = instance.volumes.all()
            
            for volume in volumes:
                
                logger.info ("Volume Id {}".format(volume.id))
                
                volume_obj = ec2.Volume(volume.id)
                
                #Assign instance tags to volumes 
                volume_obj.create_tags(Tags=instance_tags)
        
        else:
            
            logger.info ("{} : does not have tags information".format(i.id))
    else:
        logger.info("ec2 instances not available for the region")        
        
    #print (response)
    return True
