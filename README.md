# 🚀 gp2-to-gp3-volume-conversion

> Automatically enforce your organization's EBS volume policy by converting all `gp2` volumes to `gp3` — seamlessly and automatically using AWS Lambda, EventBridge, and CloudWatch.

---

## 📘 Table of Contents

- [📖 Project Overview](#-project-overview)
- [⚙️ Architecture & AWS Services Used](#-architecture--aws-services-used)
- [🧠 How It Works](#-how-it-works)
- [🚀 Deployment Guide](#-deployment-guide)
- [🧾 IAM Permissions](#-iam-permissions)
- [✅ Benefits](#-benefits)
- [🔮 Future Enhancements](#-future-enhancements)
- [📝 License](#-license)
- [🙋‍♀️ Author](#-author)

---

## 📁 Project Structure

```
gp2-to-gp3-volume-conversion/
├── lambda.py # Main AWS Lambda function code
├── README.md # Project documentation
├── architecture-diagram.png # AWS architecture image

```
---

## 📖 Project Overview

When new developers join or unintentionally create EBS volumes with type `gp2`, this project ensures such volumes are **automatically converted to `gp3`**, maintaining the company's infrastructure compliance and cost-efficiency standards.

This automation reduces manual oversight, ensures consistency, and follows best practices for EBS volume management.

---

# Architecture Diagrams

<img width="1536" height="1024" alt="gp2-gp3-diagram" src="https://github.com/user-attachments/assets/329be3ae-1277-4df7-8506-a436022300c0" />

---

## ⚙️ Architecture & AWS Services Used

This solution is built entirely with serverless components:

- **AWS Lambda**: Python function that performs the `gp2 → gp3` conversion.
- **Amazon EventBridge**: Triggers the Lambda function on EBS volume creation.
- **Amazon CloudWatch**:  Detects EBS volume creation events.

---

## 🧠 How It Works

1. A developer creates an EBS volume via console, CLI, or API.
2.  **CloudWatch** captures this event and forwards it via **EventBridge**.
3. **EventBridge** detects this event and routes it to **Lambda**.
4. **Lambda** checks if the volume is of type `gp2`:
   - If yes, it calls `ModifyVolume` to convert it to `gp3`.
   - If not, it exits without changes.

---

## 🚀 Deployment Guide

### 🔹 Step 1: Create the EventBridge Rule

In AWS Console → **EventBridge**:

- Create a new rule that listens to volume creation events.
- Use the following event pattern:

```json
{
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Volume State-change Notification"],
  "detail": {
    "state": ["available"]
  }
}
```
---

### 🔹 Step 2: Create the Lambda Function

- **Runtime**: Python 3.8 or above

- **Permissions**: Attach an IAM role with the permissions described below
            
---

### 🔹 Step 3: Assign IAM Role to Lambda

Attach a policy to allow Lambda to describe and modify volumes.

```bash
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
```
---

### 🔹 Step 4: Connect Lambda to EventBridge

 - In EventBridge, set the target of your rule to the Lambda function created.

 - Enable the rule. 

---

### 🔹 Step 5: Test the Setup

1.Manually create an EBS volume using the gp2 type.

2.Wait a few seconds.

3.Confirm:

 - The Lambda function is triggered.

 - The volume is modified to gp3 automatically.

---

# 🧾 IAM Permissions

 Ensure the Lambda function's execution role includes:

  - ec2:DescribeVolumes

  - ec2:ModifyVolume

You can expand this policy for logging, monitoring, or further automation.  

---

# ✅ Benefits

-🛡️ Enforces Standards: Ensures all volumes use gp3 as per company policy.

-💸 Cost-Efficient: gp3 offers better performance at a lower price.

-⚙️ Fully Automated: No manual intervention required.

-🧱 Scalable & Reliable: Works across all regions and teams.    

---

# 🔮 Future Enhancements

📊 Logging to CloudWatch Logs for audit.

📩 SNS notifications for conversion success/failure.

🔐 Tag-based filtering to exclude specific volumes.

📏 AWS Config integration for compliance tracking.

---

 ### 🔄 Before & After Conversion

---
- **Before:** Developer creates `EBS Volume (gp2)`

<img width="1165" height="583" alt="Before-Volume-Snap-gp2" src="https://github.com/user-attachments/assets/229b983b-cf33-40fd-bd62-64256ee367bc" />

---

- **After:** Automation ensures it becomes `EBS Volume (gp3)`
---

<img width="1154" height="562" alt="After-Volume-Snap-gp3" src="https://github.com/user-attachments/assets/ea46c677-3e59-4f0b-8e52-5156d8883d43" />

---   

Dummy Comment
