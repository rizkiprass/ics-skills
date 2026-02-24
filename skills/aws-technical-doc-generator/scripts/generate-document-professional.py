#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Technical Document Generator - Professional Format
Generates formatted technical documentation from AWS resource scan data using professional template.
"""

import json
import sys
import io
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def get_project_root():
    """Get the project root directory (where .kiro folder exists)."""
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / '.kiro').exists():
            return parent
    return Path.cwd()

class ProfessionalTechnicalDocumentGenerator:
    def __init__(self, scan_data: Dict[str, Any], customer_name: str, 
                 project_name: str, version: str = "1.0", author: str = "PT. Innovation Cloud Services"):
        """Initialize document generator with scan data and metadata."""
        self.scan_data = scan_data
        self.customer_name = customer_name
        self.project_name = project_name
        self.version = version
        self.author = author
        self.metadata = scan_data.get('metadata', {})
        self.region = self.metadata.get('region', 'ap-southeast-3')
        self.account_id = self.metadata.get('account_id', 'N/A')
    
    @staticmethod
    def get_tag_value(tags: List[Dict], key: str) -> str:
        """Extract value from AWS tags list."""
        if not tags:
            return "N/A"
        for tag in tags:
            if tag.get('Key') == key:
                return tag.get('Value', 'N/A')
        return "N/A"
    
    @staticmethod
    def get_instance_specs(instance_type: str) -> tuple:
        """Get CPU and Memory specs for common instance types."""
        specs = {
            't3.micro': ('2', '1'), 't3.small': ('2', '2'), 't3.medium': ('2', '4'),
            't3.large': ('2', '8'), 't3.xlarge': ('4', '16'), 't3.2xlarge': ('8', '32'),
            't2.micro': ('1', '1'), 't2.small': ('1', '2'), 't2.medium': ('2', '4'),
            't2.large': ('2', '8'), 'm5.large': ('2', '8'), 'm5.xlarge': ('4', '16'),
            'm5.2xlarge': ('8', '32'), 'c5.large': ('2', '4'), 'c5.xlarge': ('4', '8'),
            'r5.large': ('2', '16'), 'r5.xlarge': ('4', '32'),
        }
        return specs.get(instance_type, ('N/A', 'N/A'))
        
    def generate_cover_page(self) -> str:
        """Generate cover page."""
        return f"""**Technical Document**

**{self.author} - {self.customer_name}**

{self.project_name}

Designated for: {self.customer_name}

Prepared by:

{self.author}

Menara Caraka, 7th Floor, Jl. Dr. Ide Anak Agung Gde Agung

Kuningan Timur, Jakarta 12950, Indonesia

Email: support@icscompute.com

www.icscompute.com

"""

    def generate_toc(self) -> str:
        """Generate table of contents."""
        return """# List of Content

Contents

"""

    def generate_confidentiality(self) -> str:
        """Generate confidentiality agreement."""
        return f"""# Confidentiality Agreement

The information in this document shall not be disclosed outside of the {self.customer_name} organization and shall not be duplicated, used or disclosed in whole or in part for any purpose other than to evaluate this document. {self.customer_name} shall have the right to duplicate, use or disclose the information to the extent provided by the contract. This restriction does not limit the right of {self.customer_name} to use the information contained in this document if it is obtained from another source and developed from the existing know-how and experience of {self.customer_name}.

Copyright © {self.author}

"""

    def generate_document_control(self) -> str:
        """Generate document control section."""
        current_date = datetime.now().strftime("%d-%m-%Y")
        
        return f"""# Document Control

## Document Information

| Client | : | {self.customer_name} |
| --- | --- | --- |
| Project Name | : | {self.project_name} |
| Author | : | {self.author} |

| Version | Date | Prepared By | Description |
| --- | --- | --- | --- |
| {self.version} | {current_date} | Cloud Engineering Team | Initial Version |
|  |  |  |  |
|  |  |  |  |

## Distribution List

| Name | Organization | Email |
| --- | --- | --- |
| {self.customer_name} | {self.customer_name} |  |
| ICS Team | {self.author} | support@icscompute.com |

## Document Acceptance

The signatories below confirm that the implementation document has met the specified requirements.

| {self.author} | {self.customer_name} |
| --- | --- |
| Signature | Signature |
| TD Creator | {self.customer_name} |
| Cloud Engineering Team |  |
| {datetime.now().strftime("%B %d, %Y")} | {datetime.now().strftime("%B %d, %Y")} |

After approving this document, any changes require a change request, as they may affect the project milestone. {self.author} will assume that this document is entirely accepted by the Customer without modification if there are no questions or acknowledgement within seven (7) days.

"""

    def generate_solution_overview(self) -> str:
        """Generate AWS solution overview."""
        return f"""# Section 1 : AWS Solution Overview

## 1.1 AWS Architecture Diagram

*Figure 1. AWS Architecture Diagram*

Specification:

Region: {self.region}

**AWS Services Deployed:**
- Internet Gateway
- NAT Gateway
- Elastic Compute Cloud (EC2)
- Amazon CloudWatch
- Amazon CloudTrail
- AWS Backup
- AWS GuardDuty (Recommended)
- IAM

"""

    def generate_convention_name(self) -> str:
        """Generate naming convention table."""
        customer_short = self.customer_name.split()[0] if self.customer_name else "CUSTOMER"
        
        return f"""# Section 2 : AWS Resource List

## 2.1 AWS Convention Name

Nearly all AWS resources can be named. These should follow a consistent pattern to enable more precise identification and context. The standard naming convention described below should be used.

*Table 1. Convention Name {self.region} Region*

| No | AWS Resource | Recipe | Name Example | Tagging |
| --- | --- | --- | --- | --- |
| 1 | VPC | <customer>-<Environment>-VPC | {customer_short}-production-vpc | Environment Name |
| 2 | Internet Gateway | <customer>-<Environment>-igw | {customer_short}-production-igw | Environment Name |
| 3 | Subnet | <customer>-<Environment>-subnet-<AZ> | {customer_short}-Prod-Sub-Private-3A | Environment Name |
| 4 | Routing Tables | <customer>-<Environment>-<Public/Private>-RTB | {customer_short}-Prod-Public-RTB | Environment Name |
| 5 | NAT | <customer>-<Environment>-NAT | {customer_short}-Prod-NAT | Environment Name |
| 6 | Elastic IP | <customer>-<Environment>-EIP-<ResourceName> | {customer_short}-Prod-App-EIP | Environment Name |
| 7 | EC2 | <Customer>-<Environment>-<ResourceName> | {customer_short}-Prod-App | Environment Name |
| 8 | EBS | <EC2 Name>-EBS | App-EBS | Environment Name |
| 9 | Security Group | <customer><Environment>-<ResourceType>-<resource name>-SG | {customer_short}-Prod-EC2-App-SG | Environment Name |

"""

    def generate_vpc_section(self) -> str:
        """Generate VPC section."""
        vpc_data = self.scan_data.get('vpc', {})
        vpcs = vpc_data.get('vpcs', [])
        
        content = """## 2.2 VPC

VPC will use /16 CIDR block with the following details:

*Table 2. VPC Resource*

| No | Name | VPC ID | IPv4 CIDR | Network ACL | Route table |
| --- | --- | --- | --- | --- | --- |
"""
        
        if not vpcs:
            content += "| 1 | N/A | N/A | N/A | N/A | N/A |\n"
        else:
            for idx, vpc in enumerate(vpcs, 1):
                name = self.get_tag_value(vpc.get('Tags', []), 'Name')
                vpc_id = vpc.get('VpcId', 'N/A')
                cidr = vpc.get('CidrBlock', 'N/A')
                content += f"| {idx} | {name} | {vpc_id} | {cidr} | N/A | N/A |\n"
        
        content += "\n"
        return content

    def generate_subnet_section(self) -> str:
        """Generate subnet section."""
        vpc_data = self.scan_data.get('vpc', {})
        subnets = vpc_data.get('subnets', [])
        
        content = f"""## 2.3 Subnet

*Table 3. Subnet {self.region} Resource*

| No | Name | Subnet ID | Availability Zone | IPv4 CIDR | Route table |
| --- | --- | --- | --- | --- | --- |
"""
        
        if not subnets:
            content += "| 1 | N/A | N/A | N/A | N/A | N/A |\n"
        else:
            for idx, subnet in enumerate(subnets, 1):
                name = self.get_tag_value(subnet.get('Tags', []), 'Name')
                subnet_id = subnet.get('SubnetId', 'N/A')
                az = subnet.get('AvailabilityZone', 'N/A')
                cidr = subnet.get('CidrBlock', 'N/A')
                content += f"| {idx} | {name} | {subnet_id} | {az} | {cidr} | N/A |\n"
        
        content += "\n"
        return content

    def generate_ec2_section(self) -> str:
        """Generate EC2 section."""
        ec2_data = self.scan_data.get('ec2', {})
        instances = ec2_data.get('instances', [])
        ebs_data = self.scan_data.get('ebs', {})
        volumes = ebs_data.get('volumes', [])
        
        # Create volume map by instance
        volume_map = {}
        for vol in volumes:
            for attachment in vol.get('Attachments', []):
                instance_id = attachment.get('InstanceId')
                if instance_id:
                    if instance_id not in volume_map:
                        volume_map[instance_id] = []
                    volume_map[instance_id].append(vol.get('Size', 0))
        
        content = """## 2.4 EC2

*Table 4. EC2 Resource*

| No | Name | Instance ID | Instance Type | CPU | Memory (GB) | Disk (GB) | Platform |
| --- | --- | --- | --- | --- | --- | --- | --- |
"""
        
        if not instances:
            content += "| 1 | N/A | N/A | N/A | N/A | N/A | N/A | Linux |\n"
        else:
            for idx, instance in enumerate(instances, 1):
                name = self.get_tag_value(instance.get('Tags', []), 'Name')
                instance_id = instance.get('InstanceId', 'N/A')
                instance_type = instance.get('InstanceType', 'N/A')
                
                cpu, memory = self.get_instance_specs(instance_type)
                
                # Get disk size
                disks = volume_map.get(instance_id, [])
                disk = str(sum(disks)) if disks else "N/A"
                
                platform = instance.get('PlatformDetails', 'Linux/UNIX').replace('/UNIX', '')
                
                content += f"| {idx} | {name} | {instance_id} | {instance_type} | {cpu} | {memory} | {disk} | {platform} |\n"
        
        content += "\n"
        
        # Add IP addresses table
        content += """The following table lists public, private and elastic IPs:

*Table 5. Public, Private and Elastic IP in EC2*

| No | Name | Instance ID | Public IP | Private IP |
| --- | --- | --- | --- | --- |
"""
        
        if not instances:
            content += "| 1 | N/A | N/A | N/A | N/A |\n"
        else:
            for idx, instance in enumerate(instances, 1):
                name = self.get_tag_value(instance.get('Tags', []), 'Name')
                instance_id = instance.get('InstanceId', 'N/A')
                public_ip = instance.get('PublicIpAddress', 'N/A')
                private_ip = instance.get('PrivateIpAddress', 'N/A')
                
                content += f"| {idx} | {name} | {instance_id} | {public_ip} | {private_ip} |\n"
        
        content += "\n"
        return content

    def generate_security_groups_section(self) -> str:
        """Generate security groups section."""
        sg_data = self.scan_data.get('security_groups', {})
        security_groups = sg_data.get('security_groups', [])
        
        content = """## 2.5 Security Groups

The following security groups are configured:

*Table 6. Security Groups List*

| No | Security Group Name | Security Group ID | Description |
| --- | --- | --- | --- |
"""
        
        if not security_groups:
            content += "| 1 | N/A | N/A | N/A |\n"
        else:
            for idx, sg in enumerate(security_groups, 1):
                name = sg.get('GroupName', 'N/A')
                sg_id = sg.get('GroupId', 'N/A')
                description = sg.get('Description', 'N/A')
                content += f"| {idx} | {name} | {sg_id} | {description} |\n"
        
        content += "\n"
        
        # Add inbound/outbound rules for each security group
        for sg in security_groups[:3]:  # Limit to first 3 for brevity
            sg_name = sg.get('GroupName', 'Security Group')
            content += f"""**Security Group {sg_name} Inbound and Outbound Rules**

*Inbound Rules*

| Rules | Type | Protocol | Port range | Source |
| --- | --- | --- | --- | --- |
"""
            
            inbound_rules = sg.get('IpPermissions', [])
            if not inbound_rules:
                content += "| - | - | - | - | - |\n"
            else:
                for rule in inbound_rules[:5]:  # Limit to 5 rules
                    protocol = rule.get('IpProtocol', '-1')
                    if protocol == '-1':
                        rule_type = "All traffic"
                        port_range = "All"
                    else:
                        rule_type = "Custom"
                        from_port = rule.get('FromPort', 'N/A')
                        to_port = rule.get('ToPort', 'N/A')
                        port_range = f"{from_port}-{to_port}" if from_port != to_port else str(from_port)
                    
                    # Get sources
                    sources = []
                    for ip_range in rule.get('IpRanges', []):
                        sources.append(ip_range.get('CidrIp', ''))
                    for group in rule.get('UserIdGroupPairs', []):
                        sources.append(group.get('GroupId', ''))
                    
                    source = ', '.join(sources) if sources else 'N/A'
                    content += f"| Inbound | {rule_type} | {protocol} | {port_range} | {source} |\n"
            
            content += "\n*Outbound Rules*\n\n"
            content += """| Rules | Type | Protocol | Port range | Destination |
| --- | --- | --- | --- | --- |
"""
            
            outbound_rules = sg.get('IpPermissionsEgress', [])
            if not outbound_rules:
                content += "| - | - | - | - | - |\n"
            else:
                for rule in outbound_rules[:5]:
                    protocol = rule.get('IpProtocol', '-1')
                    if protocol == '-1':
                        rule_type = "All traffic"
                        port_range = "All"
                    else:
                        rule_type = "Custom"
                        from_port = rule.get('FromPort', 'N/A')
                        to_port = rule.get('ToPort', 'N/A')
                        port_range = f"{from_port}-{to_port}" if from_port != to_port else str(from_port)
                    
                    # Get destinations
                    destinations = []
                    for ip_range in rule.get('IpRanges', []):
                        destinations.append(ip_range.get('CidrIp', ''))
                    
                    destination = ', '.join(destinations) if destinations else 'N/A'
                    content += f"| Outbound Rules | {rule_type} | {protocol} | {port_range} | {destination} |\n"
            
            content += "\n"
        
        return content

    def generate_s3_section(self) -> str:
        """Generate S3 section."""
        s3_data = self.scan_data.get('s3', {})
        buckets = s3_data.get('buckets', [])
        
        content = """## 2.6 S3 Buckets

*Table 7. S3 Buckets*

| No | Bucket Name | Region | Encryption | Versioning |
| --- | --- | --- | --- | --- |
"""
        
        for idx, bucket in enumerate(buckets, 1):
            name = bucket.get('name', 'N/A')
            region = bucket.get('region', self.region)
            encryption = bucket.get('encryption', 'N/A')
            versioning = bucket.get('versioning', 'Disabled')
            
            content += f"| {idx} | {name} | {region} | {encryption} | {versioning} |\n"
        
        content += "\n"
        return content

    def generate_cloudwatch_section(self) -> str:
        """Generate CloudWatch section."""
        cw_data = self.scan_data.get('cloudwatch', {})
        alarms = cw_data.get('alarms', [])
        
        content = """## 2.7 CloudWatch

*Table 8. CloudWatch Metric Elastic Compute Cloud (EC2)*

| No | Metric Name | Statistic | Period |
| --- | --- | --- | --- |
| 1 | CPU Utilization | Average | 5 minutes |
| 2 | Disk Utilization | Average | 5 minutes |
| 3 | Memory Utilization | Average | 5 minutes |

## 2.8 CloudWatch Alarms

*Table 9. CloudWatch Alarms*

| No | Name | State | Conditions |
| --- | --- | --- | --- |
"""
        
        for idx, alarm in enumerate(alarms, 1):
            name = alarm.get('name', 'N/A')
            state = alarm.get('state', 'N/A')
            # Simplified condition display
            metric = alarm.get('metric_name', 'N/A')
            threshold = alarm.get('threshold', 'N/A')
            comparison = alarm.get('comparison_operator', 'N/A')
            condition = f"{metric} {comparison} {threshold}"
            
            content += f"| {idx} | {name} | {state} | {condition} |\n"
        
        content += "\n"
        return content

    def generate_iam_section(self) -> str:
        """Generate IAM section."""
        iam_data = self.scan_data.get('iam', {})
        users = iam_data.get('users', [])
        
        content = """## 2.9 IAM

*Table 10. IAM Users*

| No | Username | Group | Active Key Age | MFA |
| --- | --- | --- | --- | --- |
"""
        
        if not users:
            content += "| 1 | N/A | - | - | - |\n"
        else:
            for idx, user in enumerate(users, 1):
                username = user.get('UserName', 'N/A')
                groups = ', '.join(user.get('Groups', [])) if user.get('Groups') else '-'
                key_age = user.get('AccessKeyAge', '-')
                mfa = 'Enabled' if user.get('MFAEnabled') else 'Disabled'
                content += f"| {idx} | {username} | {groups} | {key_age} | {mfa} |\n"
        
        content += "\n"
        return content

    def generate_security_section(self) -> str:
        """Generate security section."""
        return """# Section 3 : Security

## 3.1 Use Encryption on EBS Volume

With Amazon EBS encryption, you aren't required to build, maintain, and secure your own key management infrastructure. Encryption operations occur on the servers that host EC2 instances, ensuring the security of both data at rest and data in transit between an instance and its attached EBS storage.

## 3.2 Identity and Access Management (IAM)

AWS Identity and Access Management (IAM) is a web service that helps you securely control access to AWS resources. You use IAM to control who is authenticated (signed in) and authorized (has permissions) to use resources.

## 3.3 Enabling CloudTrail

AWS CloudTrail is a service that enables governance, compliance, operational auditing, and risk auditing of your AWS account. With CloudTrail, you can log, continuously monitor and retain account activity related to actions across your AWS infrastructure.

"""

    def generate_cost_optimization_section(self) -> str:
        """Generate cost optimization section."""
        return """# Section 4 : Cost Optimization

## 4.1 Reserved Instance

Amazon EC2 Reserved Instances (RI) provide a significant discount (up to 72%) compared to On-Demand pricing and provide a capacity reservation when used in a specific Availability Zone.

## 4.2 Right Sizing using AWS Compute Optimizer

AWS Compute Optimizer recommends optimal AWS resources for your workloads to reduce costs and improve performance by using machine learning to analyze historical utilization metrics.

## 4.3 Scheduler Instances

A straightforward method to reduce costs is to stop using resources that are not in use and then restart them when their capacity is needed. Customers who use this solution to run instances during regular business hours can save up to 70% compared to running those instances 24 hours a day.

## 4.4 Savings Plans

Savings Plans are a flexible pricing model that offers low prices on EC2, Lambda, and Fargate usage, in exchange for a commitment to a consistent amount of usage (measured in $/hour) for a 1 or 3-year term.

## 4.5 VPC Endpoint

Without VPC endpoints configured, communications that originate from within a VPC and are destined for public AWS services must egress AWS to the public Internet to access these services. This network path incurs outbound data transfer charges.

"""

    def generate_tutorial_section(self) -> str:
        """Generate tutorial section."""
        return """# Section 5 : Tutorial

## 5.1 Create VPC

- On your Amazon console, go to VPC
- On the navigation pane, Choose Your VPC
- Choose to create VPC
- Choose VPC Only for the resource create
- Choose IPv4 CIDR manual input for the IPv4 CIDR Block
- Input your IPv4 CIDR
- Choose No IPv6 CIDR block for the IPv6 CIDR
- For Tenancy, choose Default
- (Optional) For tags, you can enter the name of your VPC
- Choose Create VPC

## 5.2 Create Subnet

- Open VPC Console
- Navigate to Subnet and Create Subnet
- Select the target VPC
- Enter Subnet Name (e.g., public-subnet-a)
- Select the Availability Zone
- Specify the Subnet CIDR block
- Click Create subnet

## 5.3 Create EC2

Amazon Elastic Compute Cloud (Amazon EC2) is a web service that provides secure, resizable computing capacity in the cloud.

- Log in to AWS Console
- Type EC2 on the Search Bar and Click on EC2
- Click on "INSTANCE" and then "LAUNCH INSTANCE"
- Enter your instance name and choose your OS
- In "INSTANCE TYPE" choose your specification CPU/Memory
- In "KEY PAIR NAME" choose your key pair
- Configure network settings and security group
- Configure storage
- Review and Launch

## 5.4 AWS Backup

### 5.4.1 Backup Resource Tagging (Automatic scheduling)

*Table 11. AWS Backup*

| No | Tag Key | Tag Value | Retention | Expired After |
| --- | --- | --- | --- | --- |
| 1 | Backup | DailyBackup | 7 Days | 7 Days |
| 2 | Backup | WeeklyBackup | 1 Month | 1 Month |

- Select The EC2 that you want to apply the backup
- Add the tag for the EC2 with **Key=Backup** and **Value=DailyBackup** or **WeeklyBackup**

## 5.5 CloudWatch Monitoring

### 5.5.1 Create Dashboard

- Open the CloudWatch console
- In the navigation pane, choose Dashboards and then Create dashboard
- Enter a name for the dashboard
- Add widgets to monitor your resources

### 5.5.2 Create Alarm

- Open the CloudWatch console
- In the navigation pane, choose Alarms, All alarms
- Choose Create alarm
- Select metric and configure conditions
- Set up notifications
- Review and create alarm

---

**Document End**
"""

    def generate_document(self) -> str:
        """Generate the complete technical document."""
        print("📝 Generating Technical Document (Professional Format)")
        print("=" * 60)
        
        document = []
        
        # Generate all sections
        document.append(self.generate_cover_page())
        document.append(self.generate_toc())
        document.append(self.generate_confidentiality())
        document.append(self.generate_document_control())
        document.append(self.generate_solution_overview())
        document.append(self.generate_convention_name())
        document.append(self.generate_vpc_section())
        document.append(self.generate_subnet_section())
        document.append(self.generate_ec2_section())
        document.append(self.generate_security_groups_section())
        document.append(self.generate_s3_section())
        document.append(self.generate_cloudwatch_section())
        document.append(self.generate_iam_section())
        document.append(self.generate_security_section())
        document.append(self.generate_cost_optimization_section())
        document.append(self.generate_tutorial_section())
        
        print("✅ Document generation complete!\n")
        return '\n'.join(document)


def main():
    """Main entry point for document generator."""
    if len(sys.argv) < 5:
        print("Usage: python generate-document-professional.py <scan_file> <customer_name> <project_name> <version>")
        sys.exit(1)
    
    scan_file = sys.argv[1]
    customer_name = sys.argv[2]
    project_name = sys.argv[3]
    version = sys.argv[4]
    
    # Load scan data
    with open(scan_file, 'r') as f:
        scan_data = json.load(f)
    
    # Generate document
    generator = ProfessionalTechnicalDocumentGenerator(scan_data, customer_name, project_name, version)
    document = generator.generate_document()
    
    # Get project root directory
    project_root = get_project_root()
    
    # Save document to project root
    filename = project_root / f"Technical-Document-{customer_name.replace(' ', '')}-{project_name.replace(' ', '')}-v{version}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(document)
    
    print(f"📄 Document saved to: {filename}")


if __name__ == '__main__':
    main()
