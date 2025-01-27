AWS EC2 Automation and Cleanup Workflow

Overview
This project automates the setup, monitoring, and cleanup of AWS EC2 instances using Python and GitHub Actions. 
It demonstrates essential DevOps skills like infrastructure provisioning, monitoring with CloudWatch, and resource cleanup to prevent unnecessary costs.

Features
Automated EC2 Setup:

Launches an EC2 instance with a user data script to configure it on boot.
Installs and starts Apache web server.
Assigns a security group for controlled SSH access.
Monitoring:

Enables CloudWatch detailed monitoring for EC2.
Sets up CloudWatch alarms for high CPU utilization.
Configures CloudWatch Logs to capture system logs (e.g., Apache logs).
S3 Integration:

Creates an S3 bucket for storage.
Uploads and manages files in the bucket.
Resource Cleanup:

Automatically terminates the EC2 instance.
Deletes associated security groups, key pairs, S3 buckets, and CloudWatch logs.
Workflow
The automation is orchestrated using GitHub Actions, which executes the following steps:

Install project dependencies.
Run a Python script to:
Launch and configure an EC2 instance.
Create and manage S3 buckets.
Set up monitoring and logging.
Execute cleanup operations to delete all resources after testing.

File Structure
```
├── ec2_automation.py   # Python script for EC2 setup
├── ec2_cleanup.py      # Python script for resource cleanup
├── requirements.txt    # Python dependencies
├── .github/
│   └── workflows/
│       └── ec2-workflow.yml   # GitHub Actions workflow
├── README.md           # Project documentation
```

Setup
1. Prerequisites
AWS Account with programmatic access (Access Key and Secret Key).
Python 3.9 or later.
AWS CLI installed and configured.
2. Configure Secrets
Add the following secrets to your GitHub repository:

AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
3. Clone the Repository

git clone https://github.com/<your-username>/ec2-automation.git
cd ec2-automation

4. Install Dependencies
pip install -r requirements.txt

Usage
Run Locally
Launch EC2 Instance:

python ec2_automation.py
Clean Up Resources:

python ec2_cleanup.py

Run via GitHub Actions
Push your code to the repository.
Navigate to the Actions tab in your repository.
Trigger the workflow manually or wait for the scheduled run.
Customization
User Data Script: Modify the user_data_script in ec2_automation.py to customize instance configuration.

Monitoring: Adjust CloudWatch alarms (e.g., thresholds, metrics) in the script.

Regions: Update the region_name parameter in boto3 calls to deploy in a different AWS region.

Future Enhancements
Automate notifications with AWS SNS.
Integrate with AWS Lambda for event-driven cleanup.
Add Terraform support for infrastructure as code.
License
This project is licensed under the MIT License. See the LICENSE file for details.
