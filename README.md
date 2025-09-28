# gp2-to-gp3-volume-conversion

## Description
This project automates the conversion of AWS EBS volumes from **GP2** to **GP3** when a volume is created with the wrong type. The solution uses AWS Lambda to monitor and modify volume types based on CloudWatch and EventBridge events. This ensures that all EBS volumes follow the company's standard practice of using **GP3** volumes, enhancing consistency and reducing manual intervention.

## Problem Statement
To enforce the company's policy of using **GP3** for all new EBS volumes, this project automatically converts any newly created **GP2** volumes into **GP3** volumes using AWS Lambda. This process is triggered by AWS CloudWatch events and routed through EventBridge.

## Architecture & Services Used
- **AWS Lambda**: Executes the conversion logic (written in Python) to automatically modify the volume type from **GP2** to **GP3**.
- **AWS CloudWatch**: Monitors events related to EBS volume creation.
- **AWS EventBridge**: Routes CloudWatch events to trigger the Lambda function.

## How It Works
1. **CloudWatch Event**: A new volume creation event is sent to CloudWatch.
2. **EventBridge Rule**: The CloudWatch event is routed through EventBridge.
3. **Lambda Function**: The Lambda function receives the event, checks if the volume is of type **GP2**, and converts it to **GP3**.
4. **Volume Conversion**: If the volume is a **GP2**, the Lambda function triggers the conversion process to change it to **GP3**.

## Setup Instructions
Follow these steps to deploy the solution in your AWS environment:

### 1. **Create an EventBridge Rule** to monitor volume creation events:
- Go to the **EventBridge** service in AWS Management Console.
- Create a new **rule** to capture EC2 volume creation events.
- The event pattern should capture events like `CreateVolume`.

### 2. **Create the Lambda Function**:
- Go to the **Lambda** service in the AWS Console.
- Create a new Lambda function using Python 3.8+ as the runtime.
- Assign the function an IAM role with permissions to modify EBS volumes (`ec2:ModifyVolume` and `ec2:DescribeVolumes`).

### 3. **Write the Lambda Code**:
Use the following code in your Lambda function to detect and convert GP2 volumes to GP3.

```python
import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # Extract volume ID from the event
    volume_id = event['detail']['responseElements']['volumeId']
    
    # Describe volume to check type
    response = ec2.describe_volumes(VolumeIds=[volume_id])
    volume = response['Volumes'][0]
    
    if volume['VolumeType'] == 'gp2':
        # Initiate volume type modification to GP3
        ec2.modify_volume(VolumeId=volume_id, VolumeType='gp3')
        print(f"Volume {volume_id} converted from GP2 to GP3")
    else:
        print(f"Volume {volume_id} is already GP3")
4. Assign IAM Role to Lambda:
Ensure the Lambda function has an IAM role with the following permissions:

ec2:DescribeVolumes

ec2:ModifyVolume

5. Link the Lambda Function to EventBridge:
In EventBridge, create a new target that triggers the Lambda function whenever a volume creation event is detected.

6. Test the Setup:
Create a volume in AWS and check if the Lambda function is triggered automatically to convert GP2 to GP3.

Example EventBridge Rule for CloudWatch Event Pattern
json
Copy code
{
  "source": ["aws.ec2"],
  "detail-type": ["AWS API Call via CloudTrail"],
  "detail": {
    "eventSource": ["ec2.amazonaws.com"],
    "eventName": ["CreateVolume"]
  }
}
IAM Permissions for Lambda
Ensure that your Lambda role includes the following permissions:

json
Copy code
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeVolumes",
        "ec2:ModifyVolume"
      ],
      "Resource": "*"
    }
  ]
}
Advantages
Automated Volume Type Management: Eliminates the need for manual volume type adjustments.

Cost-Effective: GP3 volumes are more cost-effective than GP2 while offering better performance.

Scalable: The system can easily scale with your AWS infrastructure, and new volume types can be added by modifying the Lambda logic.

Future Enhancements
Logging and monitoring of volume conversions for auditing.

Notifications via SNS to alert admins if the conversion fails.

Integration with AWS Config to track compliance with volume type policies.

License
This project is licensed under the MIT License - see the LICENSE file for details.


