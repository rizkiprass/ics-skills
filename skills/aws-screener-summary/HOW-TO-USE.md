# Usage Guide - AWS Service Screener Summary

This tool analyzes AWS Service Screener output (`api-full.json`), enriches the data with live information from your AWS account, and generates a summary report in `.md` and `.xlsx` format grouped by Well-Architected Framework pillars.

---

## Prerequisites

- Python 3.8+
- Python libraries:
  ```
  pip install boto3 openpyxl
  ```
- `api-full.json` file from AWS Service Screener output
- (Optional) AWS credentials for the live scan feature

---

## File Structure

```
.kiro/skills/aws-screener-summary/
├── SKILL.md                      # Skill documentation for Kiro
├── CARA-PAKAI.md                 # This file
└── scripts/
    ├── env.template              # .env template file
    ├── aws_scanner.py            # AWS account scanning script
    └── generate_xlsx.py          # Report generation script (.md & .xlsx)
```

---

## Step-by-Step Usage

### 1. Setup AWS Credentials (for Live Scan feature)

Copy the `.env` template to your project root:

```bash
copy .kiro\skills\aws-screener-summary\scripts\env.template .env
```

Edit the `.env` file and fill in your credentials:

```
AWS_ACCESS_KEY_ID=AKIAXXXXXXXXXXXXXXXX
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AWS_DEFAULT_REGION=ap-southeast-3
```

> **Important:** Add `.env` to your `.gitignore` to prevent credentials from being committed.

---

### 2. How to Use

There are 3 ways to use this tool:

#### Option A: Without AWS Scan (Simplest)

Uses only data from `api-full.json`, without enrichment from the live AWS account. The "Resource Details" column will be empty.

```bash
python .kiro/skills/aws-screener-summary/scripts/generate_xlsx.py ^
  "Service Screener - Programa/aws/779060063462/api-full.json" ^
  screener-report.xlsx ^
  --severity H ^
  --md screener-report.md
```

#### Option B: With Live Scan (Recommended)

Automatically scans the AWS account then generates the report. Resource data will be enriched with real information from AWS.

```bash
python .kiro/skills/aws-screener-summary/scripts/generate_xlsx.py ^
  "Service Screener - Programa/aws/779060063462/api-full.json" ^
  screener-report.xlsx ^
  --severity H ^
  --live-scan ^
  --env .env ^
  --md screener-report.md
```

#### Option C: Separate Scan, Then Generate

Useful if you want to save scan results for reuse.

**Step 1 - Scan AWS Account:**
```bash
python .kiro/skills/aws-screener-summary/scripts/aws_scanner.py ^
  --output aws-scan-results.json ^
  --env .env ^
  --region ap-southeast-3
```

**Step 2 - Generate Report:**
```bash
python .kiro/skills/aws-screener-summary/scripts/generate_xlsx.py ^
  "Service Screener - Programa/aws/779060063462/api-full.json" ^
  screener-report.xlsx ^
  --severity H ^
  --scan aws-scan-results.json ^
  --md screener-report.md
```

> **Note:** All output files (`screener-report.xlsx`, `screener-report.md`, `aws-scan-results.json`) are saved to the project root folder.

---

### 3. Available Parameters

#### generate_xlsx.py

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `input` | Yes | - | Path to `api-full.json` file |
| `output` | Yes | - | Output `.xlsx` file path |
| `--severity` | No | `H` | Severity filter, can be combined: `H`, `H,M`, `H,M,L`, `H,M,L,I` |
| `--md` | No | - | Output `.md` file path (if you also want to generate markdown) |
| `--scan` | No | - | Path to scan results JSON file (from `aws_scanner.py`) |
| `--live-scan` | No | - | Run a live AWS scan before generating the report |
| `--env` | No | `.env` | Path to `.env` file for credentials |
| `--region` | No | from `.env` | AWS region for live scan |

#### aws_scanner.py

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--output` | No | `aws-scan-results.json` | Output JSON file path for scan results |
| `--env` | No | `.env` | Path to `.env` file |
| `--region` | No | from `.env` | AWS region to scan |

---

## Output Columns

The generated report contains 10 columns:

| Column | Description |
|--------|-------------|
| No | Row number |
| Service | AWS service name (iam, ec2, cloudtrail, etc.) |
| Check | Short name of the finding |
| Description | Full description of the issue |
| Severity | High, Medium, Low, or Informational |
| Region | AWS region or GLOBAL |
| Affected Resources | Resource names with IDs resolved from AWS scan (e.g. `IDAS-Prod-PRP (i-044cbc7e32e4dea1d)`). Falls back to raw IDs if scan data is unavailable |
| Resource Details | Resource details from live scan (SG name, rules, ports, IAM policies, etc.) |
| Checklist | Status dropdown: Done, In Progress, Not Started, N/A |
| Note | Free-text column for reviewer notes |

---

## Excel Sheets

The report is grouped by Well-Architected Framework pillar. Each pillar becomes one sheet:

| Sheet | Code | Description |
|-------|------|-------------|
| Reliability | R | Reliability and recovery |
| Cost Optimization | C | Cost optimization |
| Performance Efficiency | P | Performance efficiency |
| Operational Excellence | O | Operational excellence |
| Security | S | Security |
| Sustainability | T | Sustainability |

> Sheets are only created if there are findings for that pillar.

---

## Excel Features

- Blue header with bold white text
- Frozen header row (stays visible when scrolling)
- Auto-filter on all columns
- Checklist column uses dropdown validation
- Arial font, thin borders, text wrapping
- Pre-adjusted column widths

---

## Data Scanned from AWS Account

| Resource | Information Collected |
|----------|---------------------|
| Security Groups | Name, description, VPC, all inbound rules (protocol, port, source IP/SG) |
| EC2 Instances | Name, instance type, state, public/private IP, attached SGs |
| VPCs | Name, CIDR block, default status |
| ELB/ALB | Type, scheme, listeners (protocol, port, SSL policy), attached SGs |
| IAM Users | MFA status, groups, attached policies |

---

## Severity Filter Examples

```bash
# High only
--severity H

# High and Medium
--severity H,M

# All severities
--severity H,M,L,I
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'boto3'` | Run `pip install boto3` |
| `ModuleNotFoundError: No module named 'openpyxl'` | Run `pip install openpyxl` |
| `NoCredentialsError` | Make sure the `.env` file is filled with valid credentials |
| `PermissionError` when saving xlsx | Close the Excel file if it's currently open |
| Resource Details column is empty | Use `--live-scan` or `--scan` to enable enrichment |
| Certain sheets are missing | No findings exist for that pillar at the selected severity |
