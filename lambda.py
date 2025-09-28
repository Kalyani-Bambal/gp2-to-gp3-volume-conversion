import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    volume_id = event['detail']['volume-id']
    
    response = ec2.describe_volumes(VolumeIds=[volume_id])
    volume = response['Volumes'][0]
    
    if volume['VolumeType'] == 'gp2':
        ec2.modify_volume(VolumeId=volume_id, VolumeType='gp3')
        print(f"✅ Volume {volume_id} converted from GP2 to GP3")
    else:
        print(f"ℹ️ Volume {volume_id} is already GP3 or not applicable")

