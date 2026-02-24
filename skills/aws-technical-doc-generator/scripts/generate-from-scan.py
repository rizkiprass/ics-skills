#!/usr/bin/env python3
"""
Generate Technical Document from Scan Results
Reads scan results from 'result scanning resource' folder and generates documentation.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

class TechnicalDocumentGenerator:
    def __init__(self, scan_file_path: str):
        """Initialize generator with scan results file."""
        self.scan_file_path = Path(scan_file_path)
        
        # Load scan results
        with open(self.scan_file_path, 'r', encoding='utf-8') as f:
            self.scan_data = json.load(f)
        
        self.metadata = self.scan_data.get('metadata', {})
        self.customer_name = self.metadata.get('customer_name', 'Customer')
        self.project_name = self.metadata.get('project_name', 'AWS Project')
        self.account_id = self.metadata.get('account_id', 'N/A')
        self.region = self.metadata.get('region', 'N/A')
        self.scan_date = self.metadata.get('scan_date', 'N/A')
    
    def get_tag_value(self, tags: List[Dict], key: str, default: str = 'N/A') -> str:
        """Extract tag value from AWS tags list."""
        if not tags:
            return default
        for tag in tags:
            if tag.get('Key') == key:
                return tag.get('Value', default)
        return default
    
    def generate_executive_summary(self) -> str:
        """Generate executive summary section."""
        ec2_count = self.scan_data.get('ec2', {}).get('total_count', 0)
        ebs_count = self.scan_data.get('ebs', {}).get('total_count', 0)
        ebs_size = self.scan_data.get('ebs', {}).get('total_size_gb', 0)
        lb_count = len(self.scan_data.get('load_balancers', {}).get('load_balancers', []))
        rds_count = self.scan_data.get('rds', {}).get('total_count', 0)
        s3_count = self.scan_data.get('s3', {}).get('total_count', 0)
        
        return f"""## 1. Executive Summary

This document provides comprehensive technical documentation for the AWS cloud infrastructure deployed for {self.customer_name}'s {self.project_name}. The infrastructure was provisioned in AWS region {self.region} and includes compute, storage, networking, and security resources.

**Key Highlights:**
- Total EC2 Instances: {ec2_count}
- Total EBS Volumes: {ebs_count} ({ebs_size} GB)
- Load Balancers: {lb_count}
- RDS Databases: {rds_count}
- S3 Buckets: {s3_count}
- Scan Date: {self.scan_date}

---
"""
    
    def generate_account_info(self) -> str:
        """Generate AWS account information section."""
        return f"""## 2. AWS Account Information

**Account ID:** {self.account_id}
**Primary Region:** {self.region}
**Scan Date:** {self.scan_date}

---
"""
    
    def generate_network_architecture(self) -> str:
        """Generate network architecture section."""
        vpc_data = self.scan_data.get('vpc', {})
        vpcs = vpc_data.get('vpcs', [])
        subnets = vpc_data.get('subnets', [])
        
        section = """## 3. Network Architecture

### 3.1 VPC Configuration

"""
        
        if vpcs:
            for vpc in vpcs:
                vpc_id = vpc.get('VpcId', 'N/A')
                cidr = vpc.get('CidrBlock', 'N/A')
                vpc_name = self.get_tag_value(vpc.get('Tags', []), 'Name', vpc_id)
                
                section += f"""**VPC: {vpc_name}**

| Property | Value |
|----------|-------|
| VPC ID | {vpc_id} |
| CIDR Block | {cidr} |
| State | {vpc.get('State', 'N/A')} |
| Default VPC | {vpc.get('IsDefault', False)} |

"""
        else:
            section += "No VPCs found.\n\n"
        
        section += "### 3.2 Subnets\n\n"
        
        if subnets:
            section += "| Subnet ID | Name | CIDR | Availability Zone | VPC ID |\n"
            section += "|-----------|------|------|-------------------|--------|\n"
            
            for subnet in subnets:
                subnet_id = subnet.get('SubnetId', 'N/A')
                subnet_name = self.get_tag_value(subnet.get('Tags', []), 'Name', subnet_id)
                cidr = subnet.get('CidrBlock', 'N/A')
                az = subnet.get('AvailabilityZone', 'N/A')
                vpc_id = subnet.get('VpcId', 'N/A')
                
                section += f"| {subnet_id} | {subnet_name} | {cidr} | {az} | {vpc_id} |\n"
            
            section += "\n"
        else:
            section += "No subnets found.\n\n"
        
        section += "---\n"
        return section
    
    def generate_compute_resources(self) -> str:
        """Generate compute resources section."""
        ec2_data = self.scan_data.get('ec2', {})
        instances = ec2_data.get('instances', [])
        
        section = """## 4. Compute Resources

### 4.1 EC2 Instances

"""
        
        if instances:
            section += f"Total Instances: {len(instances)}\n\n"
            section += "| Instance ID | Name | Type | State | Private IP | Public IP | AZ |\n"
            section += "|-------------|------|------|-------|------------|-----------|-----|\n"
            
            for instance in instances:
                instance_id = instance.get('InstanceId', 'N/A')
                instance_name = self.get_tag_value(instance.get('Tags', []), 'Name', instance_id)
                instance_type = instance.get('InstanceType', 'N/A')
                state = instance.get('State', {}).get('Name', 'N/A')
                private_ip = instance.get('PrivateIpAddress', 'N/A')
                public_ip = instance.get('PublicIpAddress', 'N/A')
                az = instance.get('Placement', {}).get('AvailabilityZone', 'N/A')
                
                section += f"| {instance_id} | {instance_name} | {instance_type} | {state} | {private_ip} | {public_ip} | {az} |\n"
            
            section += "\n"
        else:
            section += "No EC2 instances found.\n\n"
        
        section += "---\n"
        return section
    
    def generate_storage_resources(self) -> str:
        """Generate storage resources section."""
        ebs_data = self.scan_data.get('ebs', {})
        volumes = ebs_data.get('volumes', [])
        s3_data = self.scan_data.get('s3', {})
        buckets = s3_data.get('buckets', [])
        
        section = """## 5. Storage Resources

### 5.1 EBS Volumes

"""
        
        if volumes:
            section += f"Total Volumes: {len(volumes)} ({ebs_data.get('total_size_gb', 0)} GB)\n\n"
            section += "| Volume ID | Size (GB) | Type | State | Attached To | AZ |\n"
            section += "|-----------|-----------|------|-------|-------------|-----|\n"
            
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
        else:
            section += "No EBS volumes found.\n\n"
        
        section += "### 5.2 S3 Buckets\n\n"
        
        if buckets:
            section += f"Total Buckets: {len(buckets)}\n\n"
            section += "| Bucket Name | Region | Versioning | Encryption |\n"
            section += "|-------------|--------|------------|------------|\n"
            
            for bucket in buckets:
                if 'error' not in bucket:
                    name = bucket.get('name', 'N/A')
                    region = bucket.get('region', 'N/A')
                    versioning = bucket.get('versioning', 'Disabled')
                    encryption = bucket.get('encryption', 'Disabled')
                    
                    section += f"| {name} | {region} | {versioning} | {encryption} |\n"
            
            section += "\n"
        else:
            section += "No S3 buckets found.\n\n"
        
        section += "---\n"
        return section
    
    def generate_database_resources(self) -> str:
        """Generate database resources section."""
        rds_data = self.scan_data.get('rds', {})
        db_instances = rds_data.get('db_instances', [])
        
        section = """## 6. Database Resources

### 6.1 RDS Instances

"""
        
        if db_instances:
            section += f"Total RDS Instances: {len(db_instances)}\n\n"
            section += "| DB Identifier | Engine | Version | Instance Class | Storage (GB) | Multi-AZ |\n"
            section += "|---------------|--------|---------|----------------|--------------|----------|\n"
            
            for db in db_instances:
                db_id = db.get('DBInstanceIdentifier', 'N/A')
                engine = db.get('Engine', 'N/A')
                version = db.get('EngineVersion', 'N/A')
                instance_class = db.get('DBInstanceClass', 'N/A')
                storage = db.get('AllocatedStorage', 0)
                multi_az = 'Yes' if db.get('MultiAZ', False) else 'No'
                
                section += f"| {db_id} | {engine} | {version} | {instance_class} | {storage} | {multi_az} |\n"
            
            section += "\n"
        else:
            section += "No RDS instances found.\n\n"
        
        section += "---\n"
        return section
    
    def generate_load_balancing(self) -> str:
        """Generate load balancing section."""
        lb_data = self.scan_data.get('load_balancers', {})
        load_balancers = lb_data.get('load_balancers', [])
        target_groups = lb_data.get('target_groups', [])
        
        section = """## 7. Load Balancing

### 7.1 Load Balancers

"""
        
        if load_balancers:
            section += f"Total Load Balancers: {len(load_balancers)}\n\n"
            section += "| Name | Type | Scheme | DNS Name | State |\n"
            section += "|------|------|--------|----------|-------|\n"
            
            for lb in load_balancers:
                name = lb.get('LoadBalancerName', 'N/A')
                lb_type = lb.get('Type', 'N/A')
                scheme = lb.get('Scheme', 'N/A')
                dns = lb.get('DNSName', 'N/A')
                state = lb.get('State', {}).get('Code', 'N/A')
                
                section += f"| {name} | {lb_type} | {scheme} | {dns} | {state} |\n"
            
            section += "\n"
        else:
            section += "No load balancers found.\n\n"
        
        section += "### 7.2 Target Groups\n\n"
        
        if target_groups:
            section += f"Total Target Groups: {len(target_groups)}\n\n"
            section += "| Name | Protocol | Port | Target Type | Health Check |\n"
            section += "|------|----------|------|-------------|---------------|\n"
            
            for tg in target_groups:
                name = tg.get('TargetGroupName', 'N/A')
                protocol = tg.get('Protocol', 'N/A')
                port = tg.get('Port', 'N/A')
                target_type = tg.get('TargetType', 'N/A')
                health_check = tg.get('HealthCheckProtocol', 'N/A')
                
                section += f"| {name} | {protocol} | {port} | {target_type} | {health_check} |\n"
            
            section += "\n"
        else:
            section += "No target groups found.\n\n"
        
        section += "---\n"
        return section
    
    def generate_security_configuration(self) -> str:
        """Generate security configuration section."""
        sg_data = self.scan_data.get('security_groups', {})
        security_groups = sg_data.get('security_groups', [])
        
        section = """## 8. Security Configuration

### 8.1 Security Groups

"""
        
        if security_groups:
            section += f"Total Security Groups: {len(security_groups)}\n\n"
            section += "| Group ID | Name | Description | VPC ID | Inbound Rules | Outbound Rules |\n"
            section += "|----------|------|-------------|--------|---------------|----------------|\n"
            
            for sg in security_groups:
                group_id = sg.get('GroupId', 'N/A')
                group_name = sg.get('GroupName', 'N/A')
                description = sg.get('Description', 'N/A')
                vpc_id = sg.get('VpcId', 'N/A')
                inbound_count = len(sg.get('IpPermissions', []))
                outbound_count = len(sg.get('IpPermissionsEgress', []))
                
                section += f"| {group_id} | {group_name} | {description} | {vpc_id} | {inbound_count} | {outbound_count} |\n"
            
            section += "\n"
        else:
            section += "No security groups found.\n\n"
        
        section += "---\n"
        return section
    
    def generate_monitoring(self) -> str:
        """Generate monitoring section."""
        cw_data = self.scan_data.get('cloudwatch', {})
        alarms = cw_data.get('alarms', [])
        
        section = """## 9. Monitoring and Logging

### 9.1 CloudWatch Alarms

"""
        
        if alarms:
            section += f"Total CloudWatch Alarms: {len(alarms)}\n\n"
            section += "| Alarm Name | Metric | Threshold | State |\n"
            section += "|------------|--------|-----------|-------|\n"
            
            for alarm in alarms:
                alarm_name = alarm.get('AlarmName', 'N/A')
                metric = alarm.get('MetricName', 'N/A')
                threshold = alarm.get('Threshold', 'N/A')
                state = alarm.get('StateValue', 'N/A')
                
                section += f"| {alarm_name} | {metric} | {threshold} | {state} |\n"
            
            section += "\n"
        else:
            section += "No CloudWatch alarms found.\n\n"
        
        section += "---\n"
        return section
    
    def generate_document(self, version: str = '1.0') -> str:
        """Generate complete technical document."""
        doc = f"""# Technical Document
## {self.customer_name} - {self.project_name}

**Document Version:** {version}
**Date:** {datetime.now().strftime('%Y-%m-%d')}
**Prepared By:** Cloud Engineering Team

---

"""
        
        doc += self.generate_executive_summary()
        doc += self.generate_account_info()
        doc += self.generate_network_architecture()
        doc += self.generate_compute_resources()
        doc += self.generate_storage_resources()
        doc += self.generate_database_resources()
        doc += self.generate_load_balancing()
        doc += self.generate_security_configuration()
        doc += self.generate_monitoring()
        
        doc += """## 10. Appendices

### Appendix A: Scan Information

This document was automatically generated from AWS resource scan results.

**Scan File:** """ + str(self.scan_file_path.name) + """
**Scanner Version:** """ + self.metadata.get('scanner_version', 'N/A') + """

---

**Document End**
"""
        
        return doc
    
    def save_document(self, document: str, version: str = '1.0') -> str:
        """Save document to .kiro folder."""
        # Save to .kiro folder
        kiro_folder = Path.cwd() / '.kiro'
        kiro_folder.mkdir(exist_ok=True)
        
        # Generate filename
        customer_slug = self.customer_name.replace(' ', '').replace('.', '')
        project_slug = self.project_name.replace(' ', '')
        filename = f"Technical-Document-{customer_slug}-{project_slug}-v{version}.md"
        output_path = kiro_folder / filename
        
        # Save document
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(document)
        
        return str(output_path)


def main():
    """Main entry point for document generator."""
    if len(sys.argv) < 2:
        print("Usage: python generate-from-scan.py <scan_file_path> [version]")
        print("\nExample:")
        print('  python generate-from-scan.py "result scanning resource/aws-scan-Customer-20240221-143022.json" 1.0')
        sys.exit(1)
    
    scan_file = sys.argv[1]
    version = sys.argv[2] if len(sys.argv) > 2 else '1.0'
    
    if not Path(scan_file).exists():
        print(f"❌ Error: Scan file not found: {scan_file}")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("📝 Generating Technical Document")
    print("="*60 + "\n")
    
    generator = TechnicalDocumentGenerator(scan_file)
    document = generator.generate_document(version)
    output_path = generator.save_document(document, version)
    
    print(f"✅ Document generated successfully!")
    print(f"📁 Location: {output_path}")
    print(f"\nCustomer: {generator.customer_name}")
    print(f"Project: {generator.project_name}")
    print(f"Version: {version}")


if __name__ == '__main__':
    main()
