# AWS Technical Document Generator - Setup Guide

This guide will help you set up and configure the AWS Technical Document Generator skill.

## Prerequisites

### 1. Python Environment

The skill requires Python 3.7 or higher with the following packages:

```bash
# Install required packages
pip install boto3
```

### 2. AWS Account Access

You need:
- An AWS account with resources to document
- IAM credentials with read-only permissions
- Access to the AWS region(s) you want to scan

### 3. Kiro Installation

Ensure Kiro is installed and configured on your system.

## Step 1: Create IAM User for Documentation

Create a dedicated IAM user with read-only permissions:

### Using AWS Console

1. Go to IAM Console → Users → Add User
2. User name: `aws-doc-generator`
3. Access type: Programmatic access
4. Attach policy: Use the custom policy below
5. Save the Access Key ID and Secret Access Key

### Using AWS CLI

```bash
# Create IAM user
aws iam create-user --user-name aws-doc-generator

# Create access key
aws iam create-access-key --user-name aws-doc-generator

# Attach policy (after creating it)
aws iam attach-user-policy \
  --user-name aws-doc-generator \
  --policy-arn arn:aws:iam::YOUR_ACCOUNT_ID:policy/AWSDocGeneratorReadOnly
```

### IAM Policy

Create a custom policy with read-only permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ReadOnlyAccessForDocumentation",
      "Effect": "Allow",
      "Action": [
        "ec2:Describe*",
        "elasticloadbalancing:Describe*",
        "rds:Describe*",
        "s3:List*",
        "s3:GetBucket*",
        "vpc:Describe*",
        "iam:List*",
        "iam:Get*",
        "cloudwatch:Describe*",
        "cloudtrail:Describe*",
        "autoscaling:Describe*",
        "dynamodb:Describe*",
        "efs:Describe*",
        "backup:List*",
        "lambda:List*",
        "sts:GetCallerIdentity"
      ],
      "Resource": "*"
    }
  ]
}
```

**Important:** This policy provides read-only access and cannot modify any resources.

## Step 2: Configure AWS Credentials

### Option A: Environment Variables (Recommended for CI/CD)

```bash
# Add to your shell profile (~/.bashrc, ~/.zshrc, etc.)
export AWS_ACCESS_KEY_ID="your-access-key-id"
export AWS_SECRET_ACCESS_KEY="your-secret-access-key"
export AWS_DEFAULT_REGION="us-east-1"
```

### Option B: AWS Credentials File

```bash
# Create/edit ~/.aws/credentials
[default]
aws_access_key_id = your-access-key-id
aws_secret_access_key = your-secret-access-key

[doc-generator]
aws_access_key_id = your-access-key-id
aws_secret_access_key = your-secret-access-key
region = us-east-1
```

### Option C: Interactive Input (Most Secure)

Don't store credentials anywhere. The skill will prompt you each time.

## Step 3: Install the Skill

### For Kiro

The skill should already be available in `.kiro/skills/aws-technical-doc-generator/`.

Verify installation:

```bash
# List available skills
kiro skills list

# Should show: aws-technical-doc-generator
```

## Step 4: Test the Setup

### Test AWS Credentials

```bash
# Test credentials manually
aws sts get-caller-identity

# Expected output:
# {
#     "UserId": "AIDAI...",
#     "Account": "123456789012",
#     "Arn": "arn:aws:iam::123456789012:user/aws-doc-generator"
# }
```

### Test Python Dependencies

```bash
# Test boto3 installation
python3 -c "import boto3; print(boto3.__version__)"

# Expected output: 1.x.x
```

### Run a Test Scan

```bash
# Run the skill in test mode
kiro use aws-technical-doc-generator --test
```

## Step 5: Configure Skill Settings (Optional)

Edit `.kiro/skills/aws-technical-doc-generator/config.json` to customize:

```json
{
  "default_region": "us-east-1",
  "output_format": "markdown",
  "scan_services": ["ec2", "ebs", "elb", "rds", "s3", "vpc"],
  "detail_level": "comprehensive"
}
```

### Configuration Options

- **default_region**: Default AWS region to scan
- **output_format**: Document format (markdown, docx, pdf)
- **scan_services**: List of AWS services to include
- **detail_level**: Level of detail (summary, detailed, comprehensive)

## Step 6: Prepare Example Template (Optional)

If you have an existing technical document template:

1. Place it in `.kiro/skills/aws-technical-doc-generator/examples/`
2. Name it `template-technical-document.md` or `.docx`
3. The skill will analyze and follow its structure

## Common Setup Issues

### Issue 1: boto3 Not Found

```bash
# Solution: Install boto3
pip install boto3

# Or use pip3
pip3 install boto3
```

### Issue 2: AWS Credentials Invalid

```bash
# Solution: Verify credentials
aws configure list

# Check if credentials are set
echo $AWS_ACCESS_KEY_ID
```

### Issue 3: Permission Denied Errors

```bash
# Solution: Verify IAM policy is attached
aws iam list-attached-user-policies --user-name aws-doc-generator

# Should show the read-only policy
```

### Issue 4: Region Not Found

```bash
# Solution: Set default region
aws configure set region us-east-1

# Or use environment variable
export AWS_DEFAULT_REGION="us-east-1"
```

## Security Best Practices

### 1. Credential Management

- **Never commit credentials** to version control
- Use `.gitignore` to exclude credential files
- Rotate access keys every 90 days
- Use temporary credentials when possible

### 2. IAM Policy

- Use the **least privilege principle**
- Only grant read-only permissions
- Regularly review and audit permissions
- Use IAM roles instead of users when possible

### 3. Credential Storage

- Store credentials in AWS Secrets Manager (production)
- Use environment variables (development)
- Avoid hardcoding credentials in scripts

### 4. Access Logging

- Enable CloudTrail to log API calls
- Monitor for unusual access patterns
- Set up alerts for suspicious activity

## Advanced Configuration

### Multi-Region Setup

To scan multiple regions, configure region list:

```json
{
  "regions": ["us-east-1", "us-west-2", "ap-southeast-1"],
  "scan_all_regions": false
}
```

### Custom Output Templates

Create custom document templates:

1. Create template file in `references/templates/`
2. Use placeholders: `{{CUSTOMER_NAME}}`, `{{PROJECT_NAME}}`
3. Configure in `config.json`:

```json
{
  "template_file": "references/templates/custom-template.md"
}
```

### CI/CD Integration

For automated documentation in pipelines:

```yaml
# .github/workflows/aws-docs.yml
env:
  AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
  AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
  AWS_DEFAULT_REGION: us-east-1
```

## Verification Checklist

Before using the skill, verify:

- [ ] Python 3.7+ installed
- [ ] boto3 package installed
- [ ] AWS credentials configured
- [ ] IAM policy attached with read-only permissions
- [ ] Credentials tested with `aws sts get-caller-identity`
- [ ] Skill visible in `kiro skills list`
- [ ] Config file reviewed and customized
- [ ] Example template prepared (optional)

## Next Steps

After setup is complete:

1. Review the [Usage Examples](../examples/example-usage.md)
2. Run your first scan: `kiro use aws-technical-doc-generator`
3. Review the generated document
4. Customize the config file as needed
5. Set up scheduled documentation updates

## Support

If you encounter issues:

1. Check this setup guide
2. Review the troubleshooting section in README.md
3. Verify IAM permissions
4. Check AWS service quotas
5. Contact your Cloud Engineering team

## Additional Resources

- [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [AWS CLI Configuration](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)
- [AWS Security Best Practices](https://aws.amazon.com/security/best-practices/)

## Version History

- **1.0.0** (2024-02-21) - Initial setup guide

## License

This setup guide is provided as part of the AWS Technical Document Generator skill for Kiro.
