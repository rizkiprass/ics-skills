"""Scan AWS account to enrich service screener findings with live resource details."""
import json, os, sys
from pathlib import Path

try:
    import boto3
    from botocore.exceptions import ClientError, NoCredentialsError
except ImportError:
    print("ERROR: boto3 is required. Install with: pip install boto3")
    sys.exit(1)

def load_env(env_path=".env"):
    """Load .env file into environment variables."""
    p = Path(env_path)
    if not p.exists():
        return
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))

def get_session(region=None):
    """Create boto3 session from env vars or default credentials."""
    load_env()
    kwargs = {}
    if os.environ.get("AWS_ACCESS_KEY_ID"):
        kwargs["aws_access_key_id"] = os.environ["AWS_ACCESS_KEY_ID"]
    if os.environ.get("AWS_SECRET_ACCESS_KEY"):
        kwargs["aws_secret_access_key"] = os.environ["AWS_SECRET_ACCESS_KEY"]
    if os.environ.get("AWS_SESSION_TOKEN"):
        kwargs["aws_session_token"] = os.environ["AWS_SESSION_TOKEN"]
    r = region or os.environ.get("AWS_DEFAULT_REGION", "ap-southeast-3")
    kwargs["region_name"] = r
    return boto3.Session(**kwargs)

def scan_security_groups(session):
    """Get all security groups with their rules."""
    ec2 = session.client("ec2")
    result = {}
    try:
        paginator = ec2.get_paginator("describe_security_groups")
        for page in paginator.paginate():
            for sg in page["SecurityGroups"]:
                sg_id = sg["GroupId"]
                ingress_rules = []
                for rule in sg.get("IpPermissions", []):
                    proto = rule.get("IpProtocol", "-1")
                    from_port = rule.get("FromPort", "All")
                    to_port = rule.get("ToPort", "All")
                    sources = []
                    for cidr in rule.get("IpRanges", []):
                        sources.append(cidr.get("CidrIp", ""))
                    for cidr6 in rule.get("Ipv6Ranges", []):
                        sources.append(cidr6.get("CidrIpv6", ""))
                    for sg_ref in rule.get("UserIdGroupPairs", []):
                        sources.append(f"sg:{sg_ref.get('GroupId', '')}")
                    port_str = f"{from_port}" if from_port == to_port else f"{from_port}-{to_port}"
                    if proto == "-1":
                        port_str = "All"
                        proto = "All"
                    ingress_rules.append({
                        "protocol": proto,
                        "ports": port_str,
                        "sources": sources
                    })
                egress_rules = []
                for rule in sg.get("IpPermissionsEgress", []):
                    proto = rule.get("IpProtocol", "-1")
                    from_port = rule.get("FromPort", "All")
                    to_port = rule.get("ToPort", "All")
                    dests = []
                    for cidr in rule.get("IpRanges", []):
                        dests.append(cidr.get("CidrIp", ""))
                    for cidr6 in rule.get("Ipv6Ranges", []):
                        dests.append(cidr6.get("CidrIpv6", ""))
                    port_str = f"{from_port}" if from_port == to_port else f"{from_port}-{to_port}"
                    if proto == "-1":
                        port_str = "All"
                        proto = "All"
                    egress_rules.append({"protocol": proto, "ports": port_str, "destinations": dests})
                result[sg_id] = {
                    "name": sg.get("GroupName", ""),
                    "description": sg.get("Description", ""),
                    "vpc_id": sg.get("VpcId", ""),
                    "ingress": ingress_rules,
                    "egress": egress_rules,
                    "tags": {t["Key"]: t["Value"] for t in sg.get("Tags", [])}
                }
    except (ClientError, NoCredentialsError) as e:
        print(f"WARNING: Could not scan security groups: {e}")
    return result

def scan_ec2_instances(session):
    """Get all EC2 instances with details."""
    ec2 = session.client("ec2")
    result = {}
    try:
        paginator = ec2.get_paginator("describe_instances")
        for page in paginator.paginate():
            for res in page["Reservations"]:
                for inst in res["Instances"]:
                    iid = inst["InstanceId"]
                    name = ""
                    for t in inst.get("Tags", []):
                        if t["Key"] == "Name":
                            name = t["Value"]
                    sgs = [f"{sg['GroupId']} ({sg['GroupName']})" for sg in inst.get("SecurityGroups", [])]
                    result[iid] = {
                        "name": name,
                        "type": inst.get("InstanceType", ""),
                        "state": inst.get("State", {}).get("Name", ""),
                        "private_ip": inst.get("PrivateIpAddress", ""),
                        "public_ip": inst.get("PublicIpAddress", ""),
                        "vpc_id": inst.get("VpcId", ""),
                        "subnet_id": inst.get("SubnetId", ""),
                        "security_groups": sgs,
                        "platform": inst.get("PlatformDetails", ""),
                        "tags": {t["Key"]: t["Value"] for t in inst.get("Tags", [])}
                    }
    except (ClientError, NoCredentialsError) as e:
        print(f"WARNING: Could not scan EC2 instances: {e}")
    return result

def scan_vpcs(session):
    """Get all VPCs with details."""
    ec2 = session.client("ec2")
    result = {}
    try:
        resp = ec2.describe_vpcs()
        for vpc in resp["Vpcs"]:
            vid = vpc["VpcId"]
            name = ""
            for t in vpc.get("Tags", []):
                if t["Key"] == "Name":
                    name = t["Value"]
            result[vid] = {
                "name": name,
                "cidr": vpc.get("CidrBlock", ""),
                "is_default": vpc.get("IsDefault", False),
                "tags": {t["Key"]: t["Value"] for t in vpc.get("Tags", [])}
            }
    except (ClientError, NoCredentialsError) as e:
        print(f"WARNING: Could not scan VPCs: {e}")
    return result

def scan_elbs(session):
    """Get all ALBs/NLBs with listeners."""
    elbv2 = session.client("elbv2")
    result = {}
    try:
        paginator = elbv2.get_paginator("describe_load_balancers")
        for page in paginator.paginate():
            for lb in page["LoadBalancers"]:
                arn = lb["LoadBalancerArn"]
                name = lb["LoadBalancerName"]
                listeners = []
                try:
                    lresp = elbv2.describe_listeners(LoadBalancerArn=arn)
                    for l in lresp["Listeners"]:
                        listeners.append({
                            "port": l.get("Port"),
                            "protocol": l.get("Protocol", ""),
                            "ssl_policy": l.get("SslPolicy", "")
                        })
                except ClientError:
                    pass
                sgs = lb.get("SecurityGroups", [])
                result[name] = {
                    "arn": arn,
                    "type": lb.get("Type", ""),
                    "scheme": lb.get("Scheme", ""),
                    "dns": lb.get("DNSName", ""),
                    "vpc_id": lb.get("VpcId", ""),
                    "security_groups": sgs,
                    "listeners": listeners
                }
    except (ClientError, NoCredentialsError) as e:
        print(f"WARNING: Could not scan ELBs: {e}")
    return result

def scan_iam_users(session):
    """Get IAM users with MFA and policy info."""
    iam = session.client("iam")
    result = {}
    try:
        paginator = iam.get_paginator("list_users")
        for page in paginator.paginate():
            for user in page["Users"]:
                uname = user["UserName"]
                mfa_devices = []
                try:
                    mresp = iam.list_mfa_devices(UserName=uname)
                    mfa_devices = [d["SerialNumber"] for d in mresp.get("MFADevices", [])]
                except ClientError:
                    pass
                groups = []
                try:
                    gresp = iam.list_groups_for_user(UserName=uname)
                    groups = [g["GroupName"] for g in gresp.get("Groups", [])]
                except ClientError:
                    pass
                policies = []
                try:
                    presp = iam.list_attached_user_policies(UserName=uname)
                    policies = [p["PolicyName"] for p in presp.get("AttachedPolicies", [])]
                except ClientError:
                    pass
                result[uname] = {
                    "arn": user.get("Arn", ""),
                    "mfa_enabled": len(mfa_devices) > 0,
                    "mfa_devices": mfa_devices,
                    "groups": groups,
                    "attached_policies": policies,
                    "create_date": str(user.get("CreateDate", ""))
                }
    except (ClientError, NoCredentialsError) as e:
        print(f"WARNING: Could not scan IAM users: {e}")
    return result

def scan_all(region=None):
    """Run all scans and return combined results."""
    session = get_session(region)
    print(f"Scanning AWS account in region: {session.region_name}...")
    data = {
        "region": session.region_name,
        "security_groups": scan_security_groups(session),
        "ec2_instances": scan_ec2_instances(session),
        "vpcs": scan_vpcs(session),
        "elbs": scan_elbs(session),
        "iam_users": scan_iam_users(session)
    }
    print(f"Scan complete: {len(data['security_groups'])} SGs, {len(data['ec2_instances'])} EC2s, "
          f"{len(data['vpcs'])} VPCs, {len(data['elbs'])} ELBs, {len(data['iam_users'])} IAM users")
    return data

def main():
    import argparse
    parser = argparse.ArgumentParser(description="AWS Account Scanner")
    parser.add_argument("--region", help="AWS region (default: from .env or ap-southeast-3)")
    parser.add_argument("--output", default="aws-scan-results.json", help="Output JSON path")
    parser.add_argument("--env", default=".env", help="Path to .env file")
    args = parser.parse_args()
    if args.env:
        load_env(args.env)
    data = scan_all(args.region)
    Path(args.output).write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
    print(f"Scan results saved: {args.output}")

if __name__ == "__main__":
    main()
