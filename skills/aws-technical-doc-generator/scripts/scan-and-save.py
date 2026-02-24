#!/usr/bin/env python3
"""
AWS Resource Scanner with Result Storage
Scans AWS account and saves results to 'result scanning resource' folder.
"""

import boto3
import json
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class AWSResourceScanner:
    def __init__(self, access_key: str, secret_key: str, region: str = 'us-east-1', customer_name: str = '', project_name: str = ''):
        """Initialize AWS clients with provided credentials."""
        self.region = region
        self.customer_name = customer_name
        self.project_name = project_name
        self.session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )
        
        # Initialize clients
        self.ec2 = self.session.client('ec2')
        self.elb = self.session.client('elbv2')
        self.rds = self.session.client('rds')
        self.s3 = self.session.client('s3')
        self.iam = self.session.client('iam')
        self.cloudwatch = self.session.client('cloudwatch')
        self.autoscaling = self.session.client('autoscaling')
        self.sts = self.session.client('sts')
        
    def validate_credentials(self) -> Dict[str, Any]:
        """Validate AWS credentials and return account information."""
        try:
            identity = self.sts.get_caller_identity()
            return {
                'valid': True,
                'account_id': identity['Account'],
                'user_arn': identity['Arn']
            }
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }
    
    def scan_vpc(self) -> Dict[str, Any]:
        """Scan VPC and networking resources."""
        print("🔍 Scanning VPC and networking...")
        
        vpcs = self.ec2.describe_vpcs()['Vpcs']
        subnets = self.ec2.describe_subnets()['Subnets']
        route_tables = self.ec2.describe_route_tables()['RouteTables']
        igws = self.ec2.describe_internet_gateways()['InternetGateways']
        nat_gws = self.ec2.describe_nat_gateways()['NatGateways']
        
        return {
            'vpcs': vpcs,
            'subnets': subnets,
            'route_tables': route_tables,
            'internet_gateways': igws,
            'nat_gateways': nat_gws
        }
    
    def scan_ec2(self) -> Dict[str, Any]:
        """Scan EC2 instances."""
        print("🔍 Scanning EC2 instances...")
        
        instances = []
        paginator = self.ec2.get_paginator('describe_instances')
        
        for page in paginator.paginate():
            for reservation in page['Reservations']:
                instances.extend(reservation['Instances'])
        
        return {
            'instances': instances,
            'total_count': len(instances)
        }
    
    def scan_ebs(self) -> Dict[str, Any]:
        """Scan EBS volumes."""
        print("🔍 Scanning EBS volumes...")
        
        volumes = self.ec2.describe_volumes()['Volumes']
        
        return {
            'volumes': volumes,
            'total_count': len(volumes),
            'total_size_gb': sum(v['Size'] for v in volumes)
        }
    
    def scan_load_balancers(self) -> Dict[str, Any]:
        """Scan Application and Network Load Balancers."""
        print("🔍 Scanning Load Balancers...")
        
        load_balancers = self.elb.describe_load_balancers()['LoadBalancers']
        target_groups = self.elb.describe_target_groups()['TargetGroups']
        
        # Get target health for each target group
        target_health = {}
        for tg in target_groups:
            try:
                health = self.elb.describe_target_health(
                    TargetGroupArn=tg['TargetGroupArn']
                )
                target_health[tg['TargetGroupArn']] = health['TargetHealthDescriptions']
            except Exception as e:
                target_health[tg['TargetGroupArn']] = []
        
        return {
            'load_balancers': load_balancers,
            'target_groups': target_groups,
            'target_health': target_health
        }
    
    def scan_rds(self) -> Dict[str, Any]:
        """Scan RDS database instances."""
        print("🔍 Scanning RDS databases...")
        
        db_instances = self.rds.describe_db_instances()['DBInstances']
        
        return {
            'db_instances': db_instances,
            'total_count': len(db_instances)
        }
    
    def scan_s3(self) -> Dict[str, Any]:
        """Scan S3 buckets."""
        print("🔍 Scanning S3 buckets...")
        
        buckets = self.s3.list_buckets()['Buckets']
        
        # Get additional bucket information
        bucket_details = []
        for bucket in buckets:
            try:
                location = self.s3.get_bucket_location(Bucket=bucket['Name'])
                versioning = self.s3.get_bucket_versioning(Bucket=bucket['Name'])
                encryption = None
                try:
                    encryption = self.s3.get_bucket_encryption(Bucket=bucket['Name'])
                except:
                    pass
                
                bucket_details.append({
                    'name': bucket['Name'],
                    'creation_date': bucket['CreationDate'].isoformat(),
                    'region': location['LocationConstraint'] or 'us-east-1',
                    'versioning': versioning.get('Status', 'Disabled'),
                    'encryption': 'Enabled' if encryption else 'Disabled'
                })
            except Exception as e:
                bucket_details.append({
                    'name': bucket['Name'],
                    'error': str(e)
                })
        
        return {
            'buckets': bucket_details,
            'total_count': len(bucket_details)
        }
    
    def scan_security_groups(self) -> Dict[str, Any]:
        """Scan security groups."""
        print("🔍 Scanning Security Groups...")
        
        security_groups = self.ec2.describe_security_groups()['SecurityGroups']
        
        return {
            'security_groups': security_groups,
            'total_count': len(security_groups)
        }
    
    def scan_iam(self) -> Dict[str, Any]:
        """Scan IAM roles and policies."""
        print("🔍 Scanning IAM resources...")
        
        try:
            roles = self.iam.list_roles()['Roles']
            users = self.iam.list_users()['Users']
            groups = self.iam.list_groups()['Groups']
            policies = self.iam.list_policies(Scope='Local')['Policies']
            
            return {
                'roles': roles,
                'users': users,
                'groups': groups,
                'policies': policies
            }
        except Exception as e:
            return {
                'error': str(e),
                'message': 'IAM access may be restricted'
            }
    
    def scan_cloudwatch(self) -> Dict[str, Any]:
        """Scan CloudWatch alarms."""
        print("🔍 Scanning CloudWatch alarms...")
        
        alarms = self.cloudwatch.describe_alarms()['MetricAlarms']
        
        return {
            'alarms': alarms,
            'total_count': len(alarms)
        }
    
    def scan_autoscaling(self) -> Dict[str, Any]:
        """Scan Auto Scaling groups."""
        print("🔍 Scanning Auto Scaling groups...")
        
        asg_groups = self.autoscaling.describe_auto_scaling_groups()['AutoScalingGroups']
        
        return {
            'auto_scaling_groups': asg_groups,
            'total_count': len(asg_groups)
        }
    
    def scan_all(self) -> Dict[str, Any]:
        """Scan all AWS resources."""
        print("\n" + "="*60)
        print("🚀 Starting AWS Resource Scan")
        print("="*60 + "\n")
        
        # Validate credentials first
        validation = self.validate_credentials()
        if not validation['valid']:
            return {
                'error': 'Invalid credentials',
                'details': validation['error']
            }
        
        print(f"✅ Credentials validated")
        print(f"   Account ID: {validation['account_id']}")
        print(f"   Region: {self.region}\n")
        
        # Scan all resources
        results = {
            'metadata': {
                'account_id': validation['account_id'],
                'region': self.region,
                'scan_date': datetime.now().isoformat(),
                'scanner_version': '1.0.0',
                'customer_name': self.customer_name,
                'project_name': self.project_name
            }
        }
        
        try:
            results['vpc'] = self.scan_vpc()
            results['ec2'] = self.scan_ec2()
            results['ebs'] = self.scan_ebs()
            results['load_balancers'] = self.scan_load_balancers()
            results['rds'] = self.scan_rds()
            results['s3'] = self.scan_s3()
            results['security_groups'] = self.scan_security_groups()
            results['iam'] = self.scan_iam()
            results['cloudwatch'] = self.scan_cloudwatch()
            results['autoscaling'] = self.scan_autoscaling()
            
            print("\n" + "="*60)
            print("✅ Scan Complete!")
            print("="*60)
            print(f"\nResources Found:")
            print(f"  - VPCs: {len(results['vpc']['vpcs'])}")
            print(f"  - EC2 Instances: {results['ec2']['total_count']}")
            print(f"  - EBS Volumes: {results['ebs']['total_count']} ({results['ebs']['total_size_gb']} GB)")
            print(f"  - Load Balancers: {len(results['load_balancers']['load_balancers'])}")
            print(f"  - RDS Instances: {results['rds']['total_count']}")
            print(f"  - S3 Buckets: {results['s3']['total_count']}")
            print(f"  - Security Groups: {results['security_groups']['total_count']}")
            print(f"  - CloudWatch Alarms: {results['cloudwatch']['total_count']}")
            print(f"  - Auto Scaling Groups: {results['autoscaling']['total_count']}")
            
        except Exception as e:
            results['error'] = str(e)
            print(f"\n❌ Error during scan: {str(e)}")
        
        return results
    
    def save_results(self, results: Dict[str, Any]) -> str:
        """Save scan results to 'result scanning resource' folder."""
        # Create folder in project root
        project_root = Path.cwd()
        result_folder = project_root / "result scanning resource"
        result_folder.mkdir(exist_ok=True)
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        customer_slug = self.customer_name.replace(' ', '').replace('.', '')
        filename = f"aws-scan-{customer_slug}-{timestamp}.json"
        output_path = result_folder / filename
        
        # Save results
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=str, ensure_ascii=False)
        
        return str(output_path)


def main():
    """Main entry point for the scanner."""
    if len(sys.argv) < 4:
        print("Usage: python scan-and-save.py <access_key> <secret_key> <region> [customer_name] [project_name]")
        sys.exit(1)
    
    access_key = sys.argv[1]
    secret_key = sys.argv[2]
    region = sys.argv[3]
    customer_name = sys.argv[4] if len(sys.argv) > 4 else ''
    project_name = sys.argv[5] if len(sys.argv) > 5 else ''
    
    scanner = AWSResourceScanner(access_key, secret_key, region, customer_name, project_name)
    results = scanner.scan_all()
    
    # Save results to 'result scanning resource' folder
    output_path = scanner.save_results(results)
    
    print(f"\n✅ Scan results saved successfully!")
    print(f"📁 Location: {output_path}")
    print(f"\nYou can now use this file to generate technical documentation.")


if __name__ == '__main__':
    main()
