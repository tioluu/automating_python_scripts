AWS EC2 Automation and Cleanup Workflow

Overview
This project automates the setup, monitoring, and cleanup of AWS EC2 instances using Python and GitHub Actions. It demonstrates essential DevOps skills, including infrastructure provisioning, monitoring with CloudWatch, and resource cleanup to prevent unnecessary costs.

---

Features
- EC2 Automation: Launch and configure EC2 instances with a user data script.
- Monitoring: Set up CloudWatch alarms and detailed monitoring.
- S3 Integration: Create and manage S3 buckets.
- Resource Cleanup: Automatically terminate EC2 instances and delete associated resources.

---

Workflow
The automation is orchestrated using GitHub Actions:

1. Install dependencies.
2. Run Python scripts to:
   - Launch and configure EC2 instances.
   - Create S3 buckets and upload files.
   - Set up monitoring and logging.
3. Clean up resources after testing.

---

File Structure
aws-automation/
├── main.py
├── ec2_instance.py
├── security_group.py
├── s3_operations.py
├── cloudwatch_alarm.py
├── user_data.sh
├── requirements.txt
├── .github/
│   └── workflows/
│       └── ec2-workflow.yml
└── README.md

---

Setup

Prerequisites
- AWS Account with programmatic access (Access Key and Secret Key).
- Python 3.9+.
- AWS CLI installed and configured.

Configure Secrets
Add these secrets to your GitHub repository:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

Clone the Repository
git clone https://github.com/<your-username>/ec2-automation.git
cd ec2-automation

Install Dependencies
pip install -r requirements.txt

---

Usage

Run Locally
1. Launch EC2 Instance:
   python main.py
2. Clean Up Resources:
   python ec2_cleanup.py

Run via GitHub Actions
1. Push your code to the repository.
2. Navigate to the Actions tab in your repository.
3. Trigger the workflow manually or wait for the scheduled run.

---

Customization
- User Data Script: Modify `user_data.sh` to customize EC2 configuration.
- Monitoring: Adjust CloudWatch alarms in `cloudwatch_alarm.py`.
- Regions: Update the `region_name` parameter in `boto3` calls.

---

Future Enhancements
- Automate notifications with AWS SNS.
- Integrate AWS Lambda for event-driven cleanup.
- Add Terraform support for infrastructure as code.

---

License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
