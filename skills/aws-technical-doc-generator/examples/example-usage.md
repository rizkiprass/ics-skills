# AWS Technical Document Generator - Usage Examples

This document provides practical examples of using the AWS Technical Document Generator skill.

## Example 1: Basic Interactive Usage

The simplest way to use the skill is through interactive mode:

```bash
# Activate the skill
kiro use aws-technical-doc-generator
```

You'll be prompted for:
1. AWS Access Key ID
2. AWS Secret Access Key
3. AWS Region
4. Customer Name
5. Project Name
6. Document Version

**Sample Interaction:**
```
🔐 AWS Credentials Required

Please provide:
1. AWS Access Key ID: AKIAIOSFODNN7EXAMPLE
2. AWS Secret Access Key: ****************************************
3. AWS Region (default: us-east-1): ap-southeast-1

✅ Credentials validated
   Account ID: 123456789012
   Region: ap-southeast-1

📝 Document Information

1. Customer Name: PT Telkom Indonesia
2. Project Name: SAP HANA Migration to AWS
3. Document Version: 1.0

🔍 Starting AWS Resource Scan...
✅ Scan Complete!

📄 Document saved to: Technical-Document-PTTelkomIndonesia-SAPHANAMigrationtoAWS-v1.0.md
```

## Example 2: Using Environment Variables

Pre-configure AWS credentials to skip the credential prompt:

```bash
# Set AWS credentials
export AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
export AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
export AWS_DEFAULT_REGION="us-east-1"

# Run the skill
kiro use aws-technical-doc-generator
```

The skill will detect the environment variables and skip credential prompts.

## Example 3: Multiple Regions

Scan resources across multiple AWS regions:

```bash
# Scan multiple regions
kiro use aws-technical-doc-generator \
  --regions "us-east-1,us-west-2,ap-southeast-1"
```

This will:
- Scan each region separately
- Combine results into a single document
- Clearly label which resources are in which region

## Example 4: Quick Scan Mode

For large environments, use quick scan to get a summary:

```bash
# Quick scan (summary only)
kiro use aws-technical-doc-generator --quick-scan
```

Quick scan mode:
- Skips detailed resource information
- Provides counts and summaries only
- Completes much faster
- Useful for initial assessment

## Example 5: Custom Sections

Add custom sections to the document:

```bash
# Add custom sections
kiro use aws-technical-doc-generator \
  --add-section "Migration Timeline" \
  --add-section "Rollback Procedures" \
  --add-section "Performance Benchmarks"
```

Custom sections will be added to the document with placeholders for manual completion.

## Example 6: Filtering Resources

Scan only specific AWS services:

```bash
# Scan only EC2 and RDS
kiro use aws-technical-doc-generator \
  --services "ec2,rds"
```

Available service filters:
- `ec2` - EC2 instances
- `ebs` - EBS volumes
- `elb` - Load balancers
- `rds` - RDS databases
- `s3` - S3 buckets
- `vpc` - VPC and networking
- `iam` - IAM resources
- `cloudwatch` - CloudWatch alarms
- `autoscaling` - Auto Scaling groups

## Example 7: Differential Documentation

Compare with a previous version to highlight changes:

```bash
# Compare with previous version
kiro use aws-technical-doc-generator \
  --compare-with "Technical-Document-v1.0.md" \
  --highlight-changes
```

Output will include:
- New resources (highlighted in green)
- Removed resources (highlighted in red)
- Modified resources (highlighted in yellow)
- Change summary section

## Example 8: Export to Multiple Formats

Generate document in multiple formats:

```bash
# Generate in Markdown, DOCX, and PDF
kiro use aws-technical-doc-generator \
  --output-format "markdown,docx,pdf"
```

Requires additional dependencies:
- `pandoc` for DOCX conversion
- `wkhtmltopdf` for PDF conversion

## Example 9: Using Python Scripts Directly

For advanced users, use the Python scripts directly:

```bash
# Step 1: Scan AWS resources
python .kiro/skills/aws-technical-doc-generator/scripts/scan-aws-resources.py \
  "AKIAIOSFODNN7EXAMPLE" \
  "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" \
  "us-east-1"

# Output: aws-resources-20240221-143022.json

# Step 2: Generate document
python .kiro/skills/aws-technical-doc-generator/scripts/generate-document.py \
  "aws-resources-20240221-143022.json" \
  "PT Bank ABC" \
  "Core Banking Migration" \
  "1.0"

# Output: Technical-Document-PTBankABC-CoreBankingMigration-v1.0.md
```

## Example 10: CI/CD Integration

Automate documentation generation in a CI/CD pipeline:

```yaml
# .github/workflows/generate-aws-docs.yml
name: Generate AWS Documentation

on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday
  workflow_dispatch:

jobs:
  generate-docs:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install boto3
      
      - name: Scan AWS Resources
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        run: |
          python .kiro/skills/aws-technical-doc-generator/scripts/scan-aws-resources.py \
            "$AWS_ACCESS_KEY_ID" \
            "$AWS_SECRET_ACCESS_KEY" \
            "us-east-1"
      
      - name: Generate Documentation
        run: |
          SCAN_FILE=$(ls aws-resources-*.json | head -n 1)
          python .kiro/skills/aws-technical-doc-generator/scripts/generate-document.py \
            "$SCAN_FILE" \
            "MyCompany" \
            "Production Environment" \
            "$(date +%Y.%m.%d)"
      
      - name: Commit Documentation
        run: |
          git config user.name "Documentation Bot"
          git config user.email "bot@example.com"
          git add Technical-Document-*.md
          git commit -m "Update AWS documentation - $(date +%Y-%m-%d)"
          git push
```

## Example 11: Scheduled Documentation Updates

Set up a cron job to generate documentation regularly:

```bash
# Add to crontab
crontab -e

# Add this line (runs every Sunday at midnight)
0 0 * * 0 /usr/local/bin/kiro use aws-technical-doc-generator --auto-mode
```

## Example 12: Resource Tagging Report

Generate a report focused on resource tagging:

```bash
# Generate tagging compliance report
kiro use aws-technical-doc-generator \
  --report-type "tagging" \
  --required-tags "Environment,Owner,CostCenter"
```

Output includes:
- Resources with all required tags
- Resources missing tags
- Tag compliance percentage
- Recommendations for improvement

## Example 13: Cost Analysis Focus

Generate a document with emphasis on cost analysis:

```bash
# Focus on cost analysis
kiro use aws-technical-doc-generator \
  --focus "cost" \
  --include-pricing
```

Includes:
- Estimated monthly costs per resource
- Cost breakdown by service
- Cost optimization recommendations
- Reserved Instance opportunities

## Example 14: Security Audit Report

Generate a security-focused document:

```bash
# Security audit report
kiro use aws-technical-doc-generator \
  --report-type "security" \
  --check-compliance "CIS-AWS"
```

Includes:
- Security group analysis
- IAM policy review
- Encryption status
- Public exposure risks
- Compliance check results

## Example 15: Disaster Recovery Documentation

Generate DR-focused documentation:

```bash
# DR documentation
kiro use aws-technical-doc-generator \
  --focus "disaster-recovery" \
  --include-backup-status
```

Includes:
- Backup configurations
- Multi-AZ deployments
- Snapshot schedules
- RTO/RPO analysis
- DR recommendations

## Sample Output Structure

Here's what a generated document looks like:

```markdown
# Technical Document
## PT Telkom Indonesia - SAP HANA Migration to AWS

**Document Version:** 1.0
**Date:** 2024-02-21
**Prepared By:** Cloud Engineering Team

---

## 1. Executive Summary

This document provides comprehensive technical documentation...

**Key Highlights:**
- Total EC2 Instances: 12
- Total EBS Volumes: 24 (2,400 GB)
- Load Balancers: 2
- RDS Databases: 3
- S3 Buckets: 8

---

## 2. Network Architecture

### 2.1 VPC Configuration

| Property | Value |
|----------|-------|
| VPC ID | vpc-0abc123def456 |
| CIDR Block | 10.0.0.0/16 |
...

## 3. Compute Resources

### 3.1 EC2 Instances

| Instance ID | Name | Type | State | Private IP | Public IP | AZ |
|-------------|------|------|-------|------------|-----------|-----|
| i-0abc123 | web-server-01 | t3.medium | running | 10.0.1.10 | 54.123.45.67 | us-east-1a |
...
```

## Tips and Best Practices

1. **Credential Security**
   - Never commit credentials to version control
   - Use IAM roles when running in AWS environments
   - Rotate access keys regularly

2. **Documentation Frequency**
   - Generate after major changes
   - Schedule weekly/monthly updates
   - Version documents properly

3. **Review Process**
   - Always review generated documents
   - Verify resource counts
   - Check for sensitive information

4. **Customization**
   - Add custom sections for project-specific needs
   - Include architecture diagrams
   - Add operational procedures

5. **Storage**
   - Store documents in version control
   - Keep historical versions
   - Share with team members

## Troubleshooting

### Issue: Credentials not working
```bash
# Test credentials manually
aws sts get-caller-identity
```

### Issue: Missing resources
```bash
# Check IAM permissions
aws iam get-user-policy --user-name your-user --policy-name your-policy
```

### Issue: Slow scanning
```bash
# Use quick scan mode
kiro use aws-technical-doc-generator --quick-scan
```

## Next Steps

After generating your document:

1. Review for accuracy
2. Add custom sections as needed
3. Include architecture diagrams
4. Share with stakeholders
5. Update regularly
6. Archive old versions

## Support

For help or questions:
- Check the main README.md
- Review the SKILL.md documentation
- Contact your Cloud Engineering team
