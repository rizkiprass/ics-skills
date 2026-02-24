---
name: aws-screener-summary
description: "Use this skill to generate a summary report from AWS Service Screener output. Triggers when the user wants to: analyze service screener JSON results (api-full.json), filter findings by severity (High, Medium, Low), categorize findings by Well-Architected pillars (Reliability, Cost Optimization, Performance Efficiency, Operational Excellence, Security, Sustainability), or produce a summary report as .md and/or .xlsx. Also triggers when the user mentions 'service screener', 'screener summary', 'screener report', or 'well-architected findings'."
---

# AWS Service Screener Summary Skill

## Overview

Parse AWS Service Screener `api-full.json` output, scan the live AWS account for resource details, enrich findings with real resource info (SG names, rules, ports, IAM policies, etc.), filter by severity, and produce a categorized summary report grouped by Well-Architected Framework pillars.

## Data Structure

The `api-full.json` file is structured as:
```
{
  "<service>": {
    "summary": {
      "<checkName>": {
        "^description": "...",
        "shortDesc": "...",
        "criticality": "H" | "M" | "L" | "I",
        "__categoryMain": "R" | "C" | "P" | "O" | "S" | "T",
        "__affectedResources": { "<region>": ["resource1", ...] }
      }
    },
    "detail": { ... }
  }
}
```

### Pillar Mapping

| Code | Pillar |
|------|--------|
| R | Reliability |
| C | Cost Optimization |
| P | Performance Efficiency |
| O | Operational Excellence |
| S | Security |
| T | Sustainability |

### Severity Mapping

| Code | Severity |
|------|----------|
| H | High |
| M | Medium |
| L | Low |
| I | Informational |

## Workflow

### Step 1: Setup AWS Credentials

Before scanning, ensure a `.env` file exists in the project root with AWS credentials. Use `scripts/env.template` as reference:

```
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_DEFAULT_REGION=ap-southeast-3
```

### Step 2: Scan AWS Account

Run the AWS scanner to collect live resource details. Output files are always saved to the project root folder.

```bash
python .kiro/skills/aws-screener-summary/scripts/aws_scanner.py --output aws-scan-results.json --env .env
```

This scans:
- Security Groups (name, description, VPC, inbound/outbound rules with ports and sources)
- EC2 Instances (name, type, state, IPs, attached SGs, platform)
- VPCs (name, CIDR, default status)
- ELBs/ALBs (type, scheme, listeners with protocols/ports/SSL, attached SGs)
- IAM Users (MFA status, groups, attached policies)

### Step 3: Generate Summary Report

All output files (`.xlsx`, `.md`, scan results) MUST be saved to the project root folder. Never save them inside the Service Screener source folder or any subfolder.

```bash
python .kiro/skills/aws-screener-summary/scripts/generate_xlsx.py <api-full.json> screener-report.xlsx --severity H --scan aws-scan-results.json --md screener-report.md
```

Or combine scan + generate in one step:

```bash
python .kiro/skills/aws-screener-summary/scripts/generate_xlsx.py <api-full.json> screener-report.xlsx --severity H --live-scan --env .env --md screener-report.md
```

**Important:** The `<api-full.json>` input path should point to wherever the Service Screener output is located, but the output `.xlsx` and `.md` files must always be in the project root.

## Output Columns

| Column | Description |
|--------|-------------|
| No | Row number |
| Service | AWS service name (iam, ec2, cloudtrail, etc.) |
| Check | Short description of the finding |
| Description | Full description of the issue |
| Severity | High, Medium, Low, or Informational |
| Region | AWS region or GLOBAL |
| Affected Resources | Resource names with IDs resolved from AWS scan (e.g. `IDAS-Prod-PRP (i-044cbc7e32e4dea1d)`). Falls back to raw IDs if scan data is unavailable |
| Resource Details | Enriched info from live AWS scan (SG rules, EC2 details, IAM policies, etc.) |
| Checklist | Dropdown: Done, In Progress, Not Started, N/A |
| Note | Free text for reviewer notes |

## XLSX Features

- One sheet per Well-Architected pillar (only pillars with findings)
- Header row: bold white text on blue background, frozen
- Checklist column: dropdown data validation (Done/In Progress/Not Started/N/A)
- Note column: free text for manual input
- Auto-filter enabled on all columns
- Arial font, professional formatting

## Resource Enrichment Details

The scanner maps resource IDs from service screener findings to live AWS data:

| Resource Pattern | Enrichment |
|-----------------|------------|
| `sg-*` | SG name, description, VPC, all inbound rules (protocol, ports, sources) |
| `i-*` | EC2 name, instance type, state, public/private IP, attached SGs |
| `vpc-*` | VPC name, CIDR block, default status |
| ELB names | ALB type, scheme, listeners (protocol, port, SSL policy), attached SGs |
| IAM usernames | MFA status, groups, attached policies |

## Notes

- Strip HTML tags from descriptions using regex
- If AWS scan is unavailable, the Resource Details column will be empty
- Default severity filter is "H" (High) unless user specifies otherwise
- The `.env` file should be in `.gitignore` to avoid committing credentials
