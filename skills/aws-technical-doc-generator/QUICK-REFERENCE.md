# Quick Reference Guide

## Generate AWS Technical Documentation

### Default: KCI Format (Professional) - RECOMMENDED

```bash
cd .kiro/skills/aws-technical-doc-generator
python scripts/generate-from-env.py
```

**Output**: `Technical-Document-[Customer]-[Project]-v[Version]-KCI.md`

**Best for**: Client-facing documentation, enterprise projects, professional presentations

---

### Alternative: Standard Format (Simple)

```bash
cd .kiro/skills/aws-technical-doc-generator
python scripts/generate-from-env-standard.py
```

**Output**: `Technical-Document-[Customer]-[Project]-v[Version].md`

**Best for**: Internal documentation, quick overviews

---

## Configuration

Edit `.env` file in the skill folder:

```bash
# AWS Credentials
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_DEFAULT_REGION=ap-southeast-3

# Project Information
PROJECT_NAME=SAP HANA Migration
CUSTOMER_NAME=PT Telkom Indonesia
DOCUMENT_VERSION=1.0
```

---

## Output Location

All generated files are saved in the **project root directory**:

```
<project-root>/
├── aws-resources-YYYYMMDD-HHMMSS.json          # Scan results
├── Technical-Document-[...].md                  # Standard format
└── Technical-Document-[...]-KCI.md             # KCI format
```

---

## Format Comparison

| Feature | Standard | KCI |
|---------|----------|-----|
| Cover Page | ❌ | ✅ |
| Confidentiality | ❌ | ✅ |
| Document Control | Basic | Full |
| Resource Tables | Basic | Comprehensive |
| Security Section | Basic | Detailed |
| Cost Optimization | ❌ | ✅ |
| Tutorials | ❌ | ✅ |

---

## Common Commands

### First Time Setup
```bash
cd .kiro/skills/aws-technical-doc-generator
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
```

### Generate Document (Default: KCI Format)
```bash
python scripts/generate-from-env.py
```

### Generate Standard Format (Alternative)
```bash
python scripts/generate-from-env-standard.py
```

### Manual Generation (if you have scan file)
```bash
# KCI Format (Default)
python scripts/generate-document-kci-format.py <scan-file> "<customer>" "<project>" "<version>"

# Standard Format
python scripts/generate-document-standard.py <scan-file> "<customer>" "<project>" "<version>"
```

---

## Troubleshooting

### Error: boto3 not found
```bash
pip install boto3
```

### Error: .env not found
```bash
cp .env.example .env
# Then edit .env with your credentials
```

### Error: Invalid credentials
Check your AWS credentials in `.env` file

### Files not in root directory
Check that you're running from the skill folder and that `.kiro` folder exists in parent directories

---

## Documentation

- **Quick Start**: `QUICKSTART.md`
- **How to Use**: `HOW-TO-USE.md`
- **KCI Format**: `README-KCI-FORMAT.md`
- **Changelog**: `CHANGELOG-OUTPUT-LOCATION.md`

---

**Need Help?** Contact Cloud Engineering Team
