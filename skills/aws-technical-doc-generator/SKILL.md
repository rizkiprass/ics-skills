---
name: aws-technical-doc-generator
description: "Use this skill when the user wants to generate AWS technical documentation, create infrastructure documentation, scan AWS resources, document AWS architecture, or produce professional technical documents for AWS cloud projects. Triggers include: mentions of 'AWS documentation', 'AWS technical doc', 'document AWS infrastructure', 'scan AWS resources', 'AWS inventory', 'AWS architecture documentation', or requests to create comprehensive documentation for AWS deployments including EC2, VPC, RDS, S3, security groups, and other AWS services."
version: 2.1.0
author: Cloud Engineering Team
created: 2026-02-20
updated: 2026-02-21
category: documentation
tags: [aws, documentation, infrastructure, cloud, technical-writing, docx, word]
license: MIT
---

# AWS Technical Document Generator

## Overview

Automate the creation of comprehensive technical documentation for AWS cloud infrastructure projects. This skill scans your AWS account, inventories all resources, and generates professional documentation following industry standards.

## What This Skill Does

1. **Scans AWS Resources**: Automatically discovers and inventories all AWS resources in your account
2. **Generates Documentation**: Creates professional technical documents with comprehensive details
3. **Multiple Formats**: Supports both Professional (detailed) and Standard (simple) formats
4. **Secure**: Uses read-only IAM permissions to safely scan your infrastructure
5. **Customizable**: Configurable via `.env` file for different projects and customers

## Key Features

- ✅ **Automated Resource Discovery**: EC2, EBS, VPC, RDS, S3, Load Balancers, Security Groups, IAM, CloudWatch
- ✅ **Professional Documentation**: Cover page, confidentiality agreement, document control, comprehensive tables
- ✅ **Multiple Output Formats**: Generates both Markdown (.md) and Word (.docx) documents
- ✅ **Security Best Practices**: Includes security recommendations and configurations
- ✅ **Cost Optimization**: Provides cost-saving recommendations
- ✅ **Step-by-Step Tutorials**: Implementation guides for common AWS tasks
- ✅ **Clean Output**: Files saved to project root, not inside skill folder
- ✅ **Baseline Template**: Reference template included for quality checks

## Quick Start

### 1. Setup

```bash
cd .kiro/skills/aws-technical-doc-generator
pip install -r requirements.txt
npm install  # Install Node.js dependencies for DOCX conversion
cp .env.example .env
```

### 2. Configure

Edit `.env` file with your AWS credentials and project information:

```bash
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=ap-southeast-3

PROJECT_NAME=Your Project Name
CUSTOMER_NAME=Your Customer Name
DOCUMENT_VERSION=1.0
```

### 3. Generate

```bash
python scripts/generate-from-env.py
```

### 4. Review

Documents will be saved to project root:
```
<project-root>/Technical-Document-[Customer]-[Project]-v[Version].md
<project-root>/Technical-Document-[Customer]-[Project]-v[Version].docx
```

Both Markdown and Word formats are generated automatically.

## Output Formats

### Professional Format (Default)

Comprehensive documentation with:
- Professional cover page
- Confidentiality agreement
- Document control & version tracking
- Detailed resource tables
- Security best practices
- Cost optimization recommendations
- Implementation tutorials

**Use for**: Client deliverables, enterprise projects, formal documentation

### Standard Format (Alternative)

Simplified documentation with:
- Basic resource listing
- Essential information only
- Quick overview format

**Use for**: Internal documentation, quick references

## Document Structure

### Professional Format Includes:

1. **Cover Page**
   - Company branding
   - Customer information
   - Project details
   - Contact information

2. **Confidentiality Agreement**
   - Legal protection clause
   - Usage restrictions
   - Copyright notice

3. **Document Control**
   - Version tracking
   - Distribution list
   - Approval signatures

4. **Section 1: AWS Solution Overview**
   - Architecture diagram placeholder
   - AWS services deployed
   - Region information

5. **Section 2: AWS Resource List**
   - Naming conventions
   - VPC & Subnets
   - EC2 instances with specifications
   - Security Groups with rules
   - S3 Buckets
   - CloudWatch Alarms
   - IAM Users

6. **Section 3: Security**
   - EBS encryption
   - IAM best practices
   - CloudTrail configuration

7. **Section 4: Cost Optimization**
   - Reserved Instances
   - Right sizing recommendations
   - Savings Plans
   - VPC Endpoints

8. **Section 5: Tutorial**
   - Create VPC
   - Create Subnet
   - Launch EC2
   - Setup AWS Backup
   - Configure CloudWatch

## AWS Resources Scanned

| Category | Resources |
|----------|-----------|
| **Networking** | VPC, Subnets, Route Tables, Internet Gateway, NAT Gateway |
| **Compute** | EC2 Instances, EBS Volumes |
| **Load Balancing** | Application Load Balancers, Network Load Balancers |
| **Database** | RDS Instances |
| **Storage** | S3 Buckets |
| **Security** | Security Groups, IAM Users |
| **Monitoring** | CloudWatch Alarms |
| **Auto Scaling** | Auto Scaling Groups |

## Configuration

### Environment Variables (.env)

```bash
# AWS Credentials (READ-ONLY recommended)
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=ap-southeast-3

# Project Information
PROJECT_NAME=SAP HANA Migration
CUSTOMER_NAME=PT Telkom Indonesia
DOCUMENT_VERSION=1.0
```

### IAM Permissions Required

The skill requires read-only access. Template policy available in `references/iam-policy-template.json`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:Describe*",
        "elasticloadbalancing:Describe*",
        "rds:Describe*",
        "s3:List*",
        "vpc:Describe*",
        "iam:List*",
        "cloudwatch:Describe*",
        "autoscaling:Describe*"
      ],
      "Resource": "*"
    }
  ]
}
```

## Usage Examples

### Basic Usage (Professional Format with DOCX)

```bash
cd .kiro/skills/aws-technical-doc-generator
python scripts/generate-from-env.py
```

This will generate both Markdown (.md) and Word (.docx) formats automatically.

### Convert Existing Markdown to DOCX

If you already have a markdown document:

```bash
node scripts/convert-md-to-docx.js Technical-Document-[Customer]-[Project]-v[Version].md
```

### Standard Format

```bash
python scripts/generate-from-env-standard.py
```

### Manual Generation

If you already have a scan file:

```bash
# Professional format (Markdown)
python scripts/generate-document-professional.py \
  aws-resources-20260221-180055.json \
  "PT Telkom Indonesia" \
  "SAP HANA Migration" \
  "1.0"

# Convert to DOCX
node scripts/convert-md-to-docx.js Technical-Document-PTTelkomIndonesia-SAPHANAMigration-v1.0.md

# Standard format
python scripts/generate-document-standard.py \
  aws-resources-20260221-180055.json \
  "PT Telkom Indonesia" \
  "SAP HANA Migration" \
  "1.0"
```

## Security Best Practices

1. **Use Read-Only Credentials**: Never use credentials with write permissions
2. **Rotate Keys Regularly**: Change access keys every 90 days
3. **Don't Commit .env**: File is already in .gitignore
4. **Review Before Sharing**: Check for sensitive information in generated documents
5. **Use Temporary Credentials**: Consider using STS assume role when possible

## DOCX Conversion

The skill automatically converts Markdown documents to professional Word (.docx) format.

### Requirements

- **Node.js**: Version 14 or higher
- **docx package**: Installed via `npm install` in skill directory

### Features

- Professional formatting with Arial font
- Proper heading styles (H1, H2, H3)
- Tables with borders and shading
- Page headers and footers
- Page numbering
- US Letter page size (8.5" x 11")
- 1-inch margins

### Manual Conversion

To convert an existing Markdown file:

```bash
cd .kiro/skills/aws-technical-doc-generator
node scripts/convert-md-to-docx.js path/to/document.md
```

The DOCX file will be created in the same directory as the Markdown file.

## Workflow

```
┌─────────────────────────────────────────┐
│ 1. Setup .env with AWS credentials      │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 2. Run: python scripts/generate-from-env.py │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 3. Scan AWS Resources (automatic)       │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 4. Generate Markdown Document           │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 5. Convert to DOCX (automatic)          │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 6. Review and Customize                 │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 7. Deliver to Client                    │
└─────────────────────────────────────────┘
```

## Output Location

All generated files are saved to the **project root directory** (not inside the skill folder):

```
<project-root>/
├── aws-resources-YYYYMMDD-HHMMSS.json                          # Scan results
├── Technical-Document-[Customer]-[Project]-v[Version].md       # Markdown format
├── Technical-Document-[Customer]-[Project]-v[Version].docx     # Word format
└── Technical-Document-[Customer]-[Project]-v[Version]-Standard.md  # Standard format
```

## Baseline Template

A complete baseline template is available in `examples/Technical-Document-Baseline-Template.md`.

**Use it for**:
- Reference for document structure
- Quality check for generated documents
- Starting point for customization
- Training team members

## Troubleshooting

### Error: boto3 not found
```bash
pip install boto3
```

### Error: .env not found
```bash
cp .env.example .env
# Edit .env with your credentials
```

### Error: Invalid credentials
- Verify AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in .env
- Check IAM user is active
- Ensure credentials have required permissions

### Error: Permission denied
- Review IAM policy permissions
- Use the template in `references/iam-policy-template.json`

### Files not appearing in project root
- Ensure you're running from the skill folder
- Check that `.kiro` folder exists in parent directories

## Documentation

- **README.md**: Main documentation
- **QUICKSTART.md**: 5-minute quick start guide
- **HOW-TO-USE.md**: Detailed usage instructions
- **QUICK-REFERENCE.md**: Command cheat sheet
- **USING-BASELINE-TEMPLATE.md**: Guide for using baseline template
- **CHANGELOG.md**: Version history and changes
- **examples/README.md**: Example documents and templates

## Version

**Current Version**: 2.0.0  
**Last Updated**: February 21, 2026

## Changelog

### v2.0.0 (2026-02-21)
- Professional format as default
- Output files saved to project root
- Generic naming (removed specific branding)
- Unified documentation
- Baseline template included

### v1.0.0 (2026-02-20)
- Initial release
- AWS resource scanning
- Basic document generation

## Support

For issues, questions, or feature requests:
- Review documentation files
- Check troubleshooting section
- Contact Cloud Engineering Team

## License

MIT License - See LICENSE file for details

---

**Maintained by**: Cloud Engineering Team  
**Skill Type**: AWS Documentation Generator  
**Category**: Infrastructure Documentation
