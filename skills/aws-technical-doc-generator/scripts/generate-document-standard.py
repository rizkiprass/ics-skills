#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Technical Document Generator
Generates formatted technical documentation from AWS resource scan data.
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
    # Navigate up from scripts/ to skill folder to .kiro/ to project root
    for parent in current.parents:
        if (parent / '.kiro').exists():
            return parent
    # Fallback to current directory
    return Path.cwd()

class TechnicalDocumentGenerator:
    def __init__(self, scan_data: Dict[str, Any], customer_name: str, 
                 project_name: str, version: str = "1.0"):
        """Initialize document generator with scan data and metadata."""
        self.scan_data = scan_data
        self.customer_name = customer_name
        self.project_name = project_name
        self.version = version
        self.metadata = scan_data.get('metadata', {})
        
    def get_tag_value(self, tags: List[Dict], key: str, default: str = 'N/A') -> str:
        """Extract tag value from AWS tags list."""
        if not tags:
            return default
        for tag in tags:
            if tag.get('Key') == key:
                return tag.get('Value', default)
        return default
    
    def generate_header(self) -> str:
        """Generate document header."""
        return f"""# Technical Document
## {self.customer_name} - {self.project_name}

**Document Version:** {self.version}  
**Date:** {datetime.now().strftime('%Y-%m-%d')}  
**Prepared By:** Cloud Engineering Team  
**AWS Account ID:** {self.metadata.get('account_id', 'N/A')}  
**Primary Region:** {self.metadata.get('region', 'N/A')}  
**Scan Date:** {self.metadata.get('scan_date', 'N/A')}

---

"""
    
    def generate_executive_summary(self) -> str:
        """Generate executive summary section."""
        ec2_count = self.scan_data.get('ec2', {}).get('total_count', 0)
        ebs_count = self.scan_data.get('ebs', {}).get('total_count', 0)
        ebs_size = self.scan_data.get('ebs', {}).get('total_size_gb', 0)
        lb_count = len(self.scan_data.get('load_balancers', {}).get('load_balancers', []))
        rds_count = self.scan_data.get('rds', {}).get('total_count', 0)
        s3_count = self.scan_data.get('s3', {}).get('total_count', 0)
        
        return f"""## 1. Executive Summary

This document provides comprehensive technical documentation for the AWS cloud infrastructure deployed for {self.customer_name}'s {self.project_name}. The infrastructure was provisioned in AWS region {self.metadata.get('region', 'N/A')} and includes compute, storage, networking, and security resources.

### Key Highlights

- **Total EC2 Instances:** {ec2_count}
- **Total EBS Volumes:** {ebs_count} ({ebs_size} GB)
- **Load Balancers:** {lb_count}
- **RDS Databases:** {rds_count}
- **S3 Buckets:** {s3_count}

---

"""
    
    def generate_vpc_section(self) -> str:
        """Generate VPC and networking section."""
        vpc_data = self.scan_data.get('vpc', {})
        vpcs = vpc_data.get('vpcs', [])
        subnets = vpc_data.get('subnets', [])
        
        section = """## 2. Network Architecture

### 2.1 VPC Configuration

"""
        
        if not vpcs:
            section += "No VPCs found.\n\n"
        else:
            for vpc in vpcs:
                vpc_id = vpc.get('VpcId', 'N/A')
                cidr = vpc.get('CidrBlock', 'N/A')
                name = self.get_tag_value(vpc.get('Tags', []), 'Name', vpc_id)
                
                section += f"""#### VPC: {name}

| Property | Value |
|----------|-------|
| VPC ID | {vpc_id} |
| CIDR Block | {cidr} |
| State | {vpc.get('State', 'N/A')} |
| Default VPC | {vpc.get('IsDefault', False)} |

"""
        
        section += """### 2.2 Subnets

"""
        
        if not subnets:
            section += "No subnets found.\n\n"
        else:
            section += """| Subnet ID | Name | CIDR | Availability Zone | Type |
|-----------|------|------|-------------------|------|
"""
            for subnet in subnets:
                subnet_id = subnet.get('SubnetId', 'N/A')
                name = self.get_tag_value(subnet.get('Tags', []), 'Name', subnet_id)
                cidr = subnet.get('CidrBlock', 'N/A')
                az = subnet.get('AvailabilityZone', 'N/A')
                subnet_type = 'Public' if subnet.get('MapPublicIpOnLaunch', False) else 'Private'
                
                section += f"| {subnet_id} | {name} | {cidr} | {az} | {subnet_type} |\n"
            
            section += "\n"
        
        section += "---\n\n"
        return section
    
    def generate_ec2_section(self) -> str:
        """Generate EC2 instances section."""
        ec2_data = self.scan_data.get('ec2', {})
        instances = ec2_data.get('instances', [])
        
        section = """## 3. Compute Resources

### 3.1 EC2 Instances

"""
        
        if not instances:
            section += "No EC2 instances found.\n\n"
        else:
            running = sum(1 for i in instances if i.get('State', {}).get('Name') == 'running')
            stopped = sum(1 for i in instances if i.get('State', {}).get('Name') == 'stopped')
            
            section += f"**Total Instances:** {len(instances)} ({running} running, {stopped} stopped)\n\n"
            
            section += """| Instance ID | Name | Type | State | Private IP | Public IP | AZ |
|-------------|------|------|-------|------------|-----------|-----|
"""
            
            for instance in instances:
                instance_id = instance.get('InstanceId', 'N/A')
                name = self.get_tag_value(instance.get('Tags', []), 'Name', instance_id)
                instance_type = instance.get('InstanceType', 'N/A')
                state = instance.get('State', {}).get('Name', 'N/A')
                private_ip = instance.get('PrivateIpAddress', 'N/A')
                public_ip = instance.get('PublicIpAddress', 'N/A')
                az = instance.get('Placement', {}).get('AvailabilityZone', 'N/A')
                
                section += f"| {instance_id} | {name} | {instance_type} | {state} | {private_ip} | {public_ip} | {az} |\n"
            
            section += "\n### 3.2 Instance Details\n\n"
            
            for instance in instances[:5]:  # Limit to first 5 for brevity
                instance_id = instance.get('InstanceId', 'N/A')
                name = self.get_tag_value(instance.get('Tags', []), 'Name', instance_id)
                instance_type = instance.get('InstanceType', 'N/A')
                ami_id = instance.get('ImageId', 'N/A')
                launch_time = instance.get('LaunchTime', 'N/A')
                
                section += f"""#### {name} ({instance_id})

- **Instance Type:** {instance_type}
- **AMI ID:** {ami_id}
- **Launch Time:** {launch_time}
- **State:** {instance.get('State', {}).get('Name', 'N/A')}
- **Private IP:** {instance.get('PrivateIpAddress', 'N/A')}
- **Public IP:** {instance.get('PublicIpAddress', 'N/A')}
- **Availability Zone:** {instance.get('Placement', {}).get('AvailabilityZone', 'N/A')}
- **VPC ID:** {instance.get('VpcId', 'N/A')}
- **Subnet ID:** {instance.get('SubnetId', 'N/A')}

"""
        
        section += "---\n\n"
        return section
    
    def generate_ebs_section(self) -> str:
        """Generate EBS volumes section."""
        ebs_data = self.scan_data.get('ebs', {})
        volumes = ebs_data.get('volumes', [])
        
        section = """## 4. Storage Resources

### 4.1 EBS Volumes

"""
        
        if not volumes:
            section += "No EBS volumes found.\n\n"
        else:
            total_size = sum(v.get('Size', 0) for v in volumes)
            section += f"**Total Volumes:** {len(volumes)} ({total_size} GB)\n\n"
            
            section += """| Volume ID | Size (GB) | Type | State | Attached To | AZ |
|-----------|-----------|------|-------|-------------|-----|
"""
            
            for volume in volumes:
                volume_id = volume.get('VolumeId', 'N/A')
                size = volume.get('Size', 0)
                vol_type = volume.get('VolumeType', 'N/A')
                state = volume.get('State', 'N/A')
                attachments = volume.get('Attachments', [])
                attached_to = attachments[0].get('InstanceId', 'N/A') if attachments else 'N/A'
                az = volume.get('AvailabilityZone', 'N/A')
                
                section += f"| {volume_id} | {size} | {vol_type} | {state} | {attached_to} | {az} |\n"
            
            section += "\n"
        
        section += "---\n\n"
        return section
    
    def generate_load_balancer_section(self) -> str:
        """Generate load balancer section."""
        lb_data = self.scan_data.get('load_balancers', {})
        load_balancers = lb_data.get('load_balancers', [])
        target_groups = lb_data.get('target_groups', [])
        
        section = """## 5. Load Balancing

### 5.1 Load Balancers

"""
        
        if not load_balancers:
            section += "No load balancers found.\n\n"
        else:
            section += """| Name | Type | Scheme | DNS Name | State |
|------|------|--------|----------|-------|
"""
            
            for lb in load_balancers:
                name = lb.get('LoadBalancerName', 'N/A')
                lb_type = lb.get('Type', 'N/A')
                scheme = lb.get('Scheme', 'N/A')
                dns_name = lb.get('DNSName', 'N/A')
                state = lb.get('State', {}).get('Code', 'N/A')
                
                section += f"| {name} | {lb_type} | {scheme} | {dns_name} | {state} |\n"
            
            section += "\n"
        
        section += """### 5.2 Target Groups

"""
        
        if not target_groups:
            section += "No target groups found.\n\n"
        else:
            section += """| Name | Protocol | Port | Health Check |
|------|----------|------|--------------|
"""
            
            for tg in target_groups:
                name = tg.get('TargetGroupName', 'N/A')
                protocol = tg.get('Protocol', 'N/A')
                port = tg.get('Port', 'N/A')
                health_check = tg.get('HealthCheckPath', 'N/A')
                
                section += f"| {name} | {protocol} | {port} | {health_check} |\n"
            
            section += "\n"
        
        section += "---\n\n"
        return section
    
    def generate_rds_section(self) -> str:
        """Generate RDS database section."""
        rds_data = self.scan_data.get('rds', {})
        db_instances = rds_data.get('db_instances', [])
        
        section = """## 6. Database Resources

### 6.1 RDS Instances

"""
        
        if not db_instances:
            section += "No RDS instances found.\n\n"
        else:
            section += """| DB Identifier | Engine | Version | Instance Class | Storage (GB) | Multi-AZ |
|---------------|--------|---------|----------------|--------------|----------|
"""
            
            for db in db_instances:
                db_id = db.get('DBInstanceIdentifier', 'N/A')
                engine = db.get('Engine', 'N/A')
                version = db.get('EngineVersion', 'N/A')
                instance_class = db.get('DBInstanceClass', 'N/A')
                storage = db.get('AllocatedStorage', 0)
                multi_az = 'Yes' if db.get('MultiAZ', False) else 'No'
                
                section += f"| {db_id} | {engine} | {version} | {instance_class} | {storage} | {multi_az} |\n"
            
            section += "\n"
        
        section += "---\n\n"
        return section
    
    def generate_s3_section(self) -> str:
        """Generate S3 buckets section."""
        s3_data = self.scan_data.get('s3', {})
        buckets = s3_data.get('buckets', [])
        
        section = """## 7. S3 Storage

### 7.1 S3 Buckets

"""
        
        if not buckets:
            section += "No S3 buckets found.\n\n"
        else:
            section += """| Bucket Name | Region | Versioning | Encryption |
|-------------|--------|------------|------------|
"""
            
            for bucket in buckets:
                name = bucket.get('name', 'N/A')
                region = bucket.get('region', 'N/A')
                versioning = bucket.get('versioning', 'N/A')
                encryption = bucket.get('encryption', 'N/A')
                
                section += f"| {name} | {region} | {versioning} | {encryption} |\n"
            
            section += "\n"
        
        section += "---\n\n"
        return section
    
    def generate_security_section(self) -> str:
        """Generate security configuration section."""
        sg_data = self.scan_data.get('security_groups', {})
        security_groups = sg_data.get('security_groups', [])
        
        section = """## 8. Security Configuration

### 8.1 Security Groups

"""
        
        if not security_groups:
            section += "No security groups found.\n\n"
        else:
            section += f"**Total Security Groups:** {len(security_groups)}\n\n"
            
            section += """| Group ID | Name | VPC ID | Inbound Rules | Outbound Rules |
|----------|------|--------|---------------|----------------|
"""
            
            for sg in security_groups[:10]:  # Limit to first 10
                group_id = sg.get('GroupId', 'N/A')
                name = sg.get('GroupName', 'N/A')
                vpc_id = sg.get('VpcId', 'N/A')
                inbound = len(sg.get('IpPermissions', []))
                outbound = len(sg.get('IpPermissionsEgress', []))
                
                section += f"| {group_id} | {name} | {vpc_id} | {inbound} | {outbound} |\n"
            
            section += "\n"
        
        section += "---\n\n"
        return section
    
    def generate_monitoring_section(self) -> str:
        """Generate monitoring and logging section."""
        cw_data = self.scan_data.get('cloudwatch', {})
        alarms = cw_data.get('alarms', [])
        
        section = """## 9. Monitoring and Logging

### 9.1 CloudWatch Alarms

"""
        
        if not alarms:
            section += "No CloudWatch alarms configured.\n\n"
        else:
            section += f"**Total Alarms:** {len(alarms)}\n\n"
            
            section += """| Alarm Name | Metric | Threshold | State |
|------------|--------|-----------|-------|
"""
            
            for alarm in alarms[:10]:  # Limit to first 10
                name = alarm.get('AlarmName', 'N/A')
                metric = alarm.get('MetricName', 'N/A')
                threshold = alarm.get('Threshold', 'N/A')
                state = alarm.get('StateValue', 'N/A')
                
                section += f"| {name} | {metric} | {threshold} | {state} |\n"
            
            section += "\n"
        
        section += "---\n\n"
        return section
    
    def generate_document(self) -> str:
        """Generate complete technical document."""
        print("\n" + "="*60)
        print("📝 Generating Technical Document")
        print("="*60 + "\n")
        
        document = ""
        document += self.generate_header()
        document += self.generate_executive_summary()
        document += self.generate_vpc_section()
        document += self.generate_ec2_section()
        document += self.generate_ebs_section()
        document += self.generate_load_balancer_section()
        document += self.generate_rds_section()
        document += self.generate_s3_section()
        document += self.generate_security_section()
        document += self.generate_monitoring_section()
        
        document += """## 10. Conclusion

This technical document provides a comprehensive overview of the AWS infrastructure deployed for this project. All resources have been documented with their current configurations and states as of the scan date.

For any questions or clarifications regarding this documentation, please contact the Cloud Engineering team.

---

**Document End**
"""
        
        print("✅ Document generation complete!\n")
        return document


def main():
    """Main entry point for document generator."""
    if len(sys.argv) < 5:
        print("Usage: python generate-document.py <scan_file> <customer_name> <project_name> <version>")
        sys.exit(1)
    
    scan_file = sys.argv[1]
    customer_name = sys.argv[2]
    project_name = sys.argv[3]
    version = sys.argv[4]
    
    # Load scan data
    with open(scan_file, 'r') as f:
        scan_data = json.load(f)
    
    # Generate document
    generator = TechnicalDocumentGenerator(scan_data, customer_name, project_name, version)
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
