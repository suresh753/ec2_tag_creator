import boto3

client = boto3.client('ec2')

Custom_Tags = {'Application' : '', 'BU' : '','Environment' : '','Name' : '','Owner' : '','Project' : ''}


def create_tag(instance,region):
    
    ec2 = boto3.resource('ec2',region_name=region)
    
    response = True
    
    # list of tags need to be created
    Tags_Create_Keys = []
    
    Instance_Tags = []
    
    Tags_Repo_Keys  = list(Custom_Tags.keys())
    
    resource_instance = ec2.Instance(instance["InstanceId"])
    for each_tag in resource_instance.tags:
        Instance_Tags.append(each_tag['Key'])   

    # Logic to compare the instance tags with defined tags

    print ("Default Tags  {} ".format(Tags_Repo_Keys))
    print ("Instance Tags {} ".format(Instance_Tags))
    Tags_Create_Keys = list(set(Tags_Repo_Keys).difference(Instance_Tags))
    
    # Tags
    Tags_Create=[ {'Key':i,'Value':Custom_Tags[i]} for i in Tags_Create_Keys ]
    print (Tags_Create)
    if not Tags_Create:
        print('All Tags are successfully created')
    else:
        response = resource_instance.create_tags(Tags=Tags_Create)
    
    return response
    
    


def lambda_handler(event, context):
    for region in client.describe_regions()['Regions']:
        ec2 = boto3.client('ec2', region_name=region['RegionName'])
        response = ec2.describe_instances()
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                print("=========================================")
                print ("Region {} {} ".format(region['RegionName'],instance["InstanceId"]))
                create_tag(instance,region['RegionName'])
            print("==============================================\n")
    return True
