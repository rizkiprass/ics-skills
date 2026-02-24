#!/usr/bin/env python3
"""
Fix and regenerate technical document with actual AWS resource data
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def get_tag_value(tags, key):
    """Extract value from AWS tags list"""
    if not tags:
        return "N/A"
    for tag in tags:
        if tag.get('Key') == key:
            return tag.get('Value', 'N/A')
    return "N/A"

def load_scan_data(json_file):
    """Load AWS scan data from JSON file"""
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_vpc_section(scan_data):
    """Generate VPC section with actual data"""
    vpc_data = scan_data.get('vpc', {})
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
            name = get_tag_value(vpc.get('Tags', []), 'Name')
            vpc_id = vpc.get('VpcId', 'N/A')
            cidr = vpc.get('CidrBlock', 'N/A')
            content += f"| {idx} | {name} | {vpc_id} | {cidr} | N/A | N/A |\n"
    
    content += "\n"
    return content

def generate_subnet_section(scan_data, region):
    """Generate subnet section with actual data"""
    vpc_data = scan_data.get('vpc', {})
    subnets = vpc_data.get('subnets', [])
    
    content = f"""## 2.3 Subnet

*Table 3. Subnet {region} Resource*

| No | Name | Subnet ID | Availability Zone | IPv4 CIDR | Route table |
| --- | --- | --- | --- | --- | --- |
"""
    
    if not subnets:
        content += "| 1 | N/A | N/A | N/A | N/A | N/A |\n"
    else:
        for idx, subnet in enumerate(subnets, 1):
            name = get_tag_value(subnet.get('Tags', []), 'Name')
            subnet_id = subnet.get('SubnetId', 'N/A')
            az = subnet.get('AvailabilityZone', 'N/A')
            cidr = subnet.get('CidrBlock', 'N/A')
            content += f"| {idx} | {name} | {subnet_id} | {az} | {cidr} | N/A |\n"
    
    content += "\n"
    return content

def get_instance_specs(instance_type):
    """Get CPU and Memory specs for common instance types"""
    specs = {
        't3.micro': ('2', '1'),
        't3.small': ('2', '2'),
        't3.medium': ('2', '4'),
        't3.large': ('2', '8'),
        't3.xlarge': ('4', '16'),
        't3.2xlarge': ('8', '32'),
        't2.micro': ('1', '1'),
        't2.small': ('1', '2'),
        't2.medium': ('2', '4'),
        't2.large': ('2', '8'),
        'm5.large': ('2', '8'),
        'm5.xlarge': ('4', '16'),
        'm5.2xlarge': ('8', '32'),
        'c5.large': ('2', '4'),
        'c5.xlarge': ('4', '8'),
        'r5.large': ('2', '16'),
        'r5.xlarge': ('4', '32'),
    }
    return specs.get(instance_type, ('N/A', 'N/A'))

def generate_ec2_section(scan_data):
    """Generate EC2 section with actual data"""
    ec2_data = scan_data.get('ec2', {})
    instances = ec2_data.get('instances', [])
    ebs_data = scan_data.get('ebs', {})
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
            name = get_tag_value(instance.get('Tags', []), 'Name')
            instance_id = instance.get('InstanceId', 'N/A')
            instance_type = instance.get('InstanceType', 'N/A')
            
            cpu, memory = get_instance_specs(instance_type)
            
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
            name = get_tag_value(instance.get('Tags', []), 'Name')
            instance_id = instance.get('InstanceId', 'N/A')
            public_ip = instance.get('PublicIpAddress', 'N/A')
            private_ip = instance.get('PrivateIpAddress', 'N/A')
            
            content += f"| {idx} | {name} | {instance_id} | {public_ip} | {private_ip} |\n"
    
    content += "\n"
    return content

def generate_security_groups_section(scan_data):
    """Generate security groups section with actual data"""
    sg_data = scan_data.get('security_groups', {})
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
    
    # Add rules for each security group
    for sg in security_groups:
        sg_name = sg.get('GroupName', 'N/A')
        content += f"""**Security Group {sg_name} Inbound and Outbound Rules**

*Inbound Rules*

| Rules | Type | Protocol | Port range | Source |
| --- | --- | --- | --- | --- |
"""
        
        inbound_rules = sg.get('IpPermissions', [])
        if not inbound_rules:
            content += "| - | - | - | - | - |\n"
        else:
            for rule in inbound_rules:
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
        content += "| Rules | Type | Protocol | Port range | Destination |\n"
        content += "| --- | --- | --- | --- | --- |\n"
        
        outbound_rules = sg.get('IpPermissionsEgress', [])
        if not outbound_rules:
            content += "| - | - | - | - | - |\n"
        else:
            for rule in outbound_rules:
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

def generate_s3_section(scan_data, region):
    """Generate S3 section with actual data"""
    s3_data = scan_data.get('s3', {})
    buckets = s3_data.get('buckets', [])
    
    content = """## 2.6 S3 Buckets

*Table 7. S3 Buckets*

| No | Bucket Name | Region | Encryption | Versioning |
| --- | --- | --- | --- | --- |
"""
    
    if not buckets:
        content += "| 1 | N/A | N/A | N/A | N/A |\n"
    else:
        for idx, bucket in enumerate(buckets, 1):
            name = bucket.get('name', 'N/A')
            encryption = bucket.get('encryption', 'N/A')
            versioning = bucket.get('versioning', 'Disabled')
            content += f"| {idx} | {name} | {region} | {encryption} | {versioning} |\n"
    
    content += "\n"
    return content

def generate_cloudwatch_section(scan_data):
    """Generate CloudWatch section"""
    cloudwatch_data = scan_data.get('cloudwatch', {})
    alarms = cloudwatch_data.get('alarms', [])
    
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
    
    if not alarms:
        content += "| - | - | - | - |\n"
    else:
        for idx, alarm in enumerate(alarms, 1):
            name = alarm.get('AlarmName', 'N/A')
            state = alarm.get('StateValue', 'N/A')
            conditions = alarm.get('AlarmDescription', 'N/A')
            content += f"| {idx} | {name} | {state} | {conditions} |\n"
    
    content += "\n"
    return content

def generate_iam_section(scan_data):
    """Generate IAM section"""
    iam_data = scan_data.get('iam', {})
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

def main():
    if len(sys.argv) < 2:
        print("Usage: python fix-document.py <scan-json-file>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    
    # Load scan data
    print(f"Loading scan data from {json_file}...")
    scan_data = load_scan_data(json_file)
    
    metadata = scan_data.get('metadata', {})
    region = metadata.get('region', 'ap-southeast-3')
    
    # Read current document
    doc_file = None
    for f in Path('.').glob('Technical-Document-*.md'):
        doc_file = f
        break
    
    if not doc_file:
        print("Error: Technical document not found!")
        sys.exit(1)
    
    print(f"Reading document {doc_file}...")
    with open(doc_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace sections
    print("Updating VPC section...")
    vpc_section = generate_vpc_section(scan_data)
    content = replace_section(content, '## 2.2 VPC', '## 2.3 Subnet', vpc_section)
    
    print("Updating Subnet section...")
    subnet_section = generate_subnet_section(scan_data, region)
    content = replace_section(content, '## 2.3 Subnet', '## 2.4 EC2', subnet_section)
    
    print("Updating EC2 section...")
    ec2_section = generate_ec2_section(scan_data)
    content = replace_section(content, '## 2.4 EC2', '## 2.5 Security Groups', ec2_section)
    
    print("Updating Security Groups section...")
    sg_section = generate_security_groups_section(scan_data)
    content = replace_section(content, '## 2.5 Security Groups', '## 2.6 S3 Buckets', sg_section)
    
    print("Updating S3 section...")
    s3_section = generate_s3_section(scan_data, region)
    content = replace_section(content, '## 2.6 S3 Buckets', '## 2.7 CloudWatch', s3_section)
    
    print("Updating CloudWatch section...")
    cw_section = generate_cloudwatch_section(scan_data)
    content = replace_section(content, '## 2.7 CloudWatch', '## 2.9 IAM', cw_section)
    
    print("Updating IAM section...")
    iam_section = generate_iam_section(scan_data)
    content = replace_section(content, '## 2.9 IAM', '# Section 3 : Security', iam_section)
    
    # Write updated document
    print(f"Writing updated document to {doc_file}...")
    with open(doc_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ Document updated successfully!")

def replace_section(content, start_marker, end_marker, new_section):
    """Replace a section in the document"""
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    if start_idx == -1 or end_idx == -1:
        return content
    
    return content[:start_idx] + new_section + content[end_idx:]

if __name__ == '__main__':
    main()
