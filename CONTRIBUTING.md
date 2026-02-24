# Contributing Guide

Thank you for contributing to the AI Agent Skills Repository! This guide covers everything you need to create a new skill that fits the repository standards.

## Quick Start

1. Copy the template directory:
   ```bash
   cp -r _template/ skills/your-skill-name/
   ```
2. Rename the directory to a descriptive, kebab-case name (e.g., `skills/aws-cost-analyzer/`).
3. Edit `skills/your-skill-name/SKILL.md` — fill in the frontmatter fields and write the skill instructions.
4. Edit `skills/your-skill-name/README.md` — write human-readable documentation for the skill.
5. Add any scripts to `scripts/` and examples to `examples/`.
6. Run through the [pre-submission checklist](#pre-submission-checklist) before opening a pull request.

## Naming Convention

Skill directories use **kebab-case** — lowercase words separated by hyphens.

Rules:
- Use descriptive, concise names that reflect what the skill does
- Start with the platform or domain when relevant (e.g., `aws-`, `cloud-`)
- Avoid abbreviations unless widely understood (e.g., `aws`, `doc`)
- The directory name must match the `name` field in `SKILL.md` frontmatter

Examples of good names:
- `aws-screener-summary`
- `cloud-sow-analyzer`
- `aws-technical-doc-generator`

Examples of bad names:
- `AwsScreener` (not kebab-case)
- `my-skill` (not descriptive)
- `aws_cost_tool` (uses underscores)

## Required Files

Every skill directory must contain:

| File | Required | Description |
|------|----------|-------------|
| `SKILL.md` | Yes | Frontmatter metadata and AI agent instructions |
| `README.md` | Recommended | Human-readable documentation |

## SKILL.md Frontmatter

The `SKILL.md` file starts with a YAML frontmatter block enclosed in `---` delimiters. This metadata is used for cataloging and discovery.

### Required Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `name` | string | Kebab-case name, must match directory name | `aws-cost-analyzer` |
| `description` | string | Short description of what the skill does | `"Analyze AWS cost reports and generate summaries"` |
| `version` | string | Semantic version | `1.0.0` |
| `author` | string | Author or team name | `Cloud Ops Team` |
| `created` | date | Creation date in ISO format | `2026-01-15` |
| `updated` | date | Last updated date in ISO format | `2026-02-01` |
| `category` | string | One of the predefined categories (see below) | `cloud-operations` |
| `tags` | string[] | Array of lowercase descriptive tags | `[aws, cost, reporting]` |

### Optional Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `platforms` | string[] | Target AI platforms | `[kiro, claude-code]` |
| `license` | string | License if different from repository (MIT) | `Apache-2.0` |
| `risk` | string | Risk level: `safe`, `moderate`, or `dangerous` | `safe` |
| `source` | string | Origin: `community` or `official` | `community` |

### Valid Categories

- `cloud-operations` — AWS and cloud management tasks
- `documentation` — Document generation and processing
- `cloud-architecture` — Architecture review and design
- `document-processing` — File conversion and manipulation
- `devops` — CI/CD, deployment, and infrastructure
- `security` — Security scanning and compliance

### Valid Platforms

- `kiro`
- `github-copilot-cli`
- `claude-code`
- `codex`

### Example Frontmatter

```yaml
---
name: aws-cost-analyzer
description: "Analyze AWS Cost Explorer data and generate monthly cost summaries"
version: 1.0.0
author: Cloud Ops Team
created: 2026-01-15
updated: 2026-01-15
category: cloud-operations
tags: [aws, cost, reporting, finops]
platforms: [kiro, claude-code]
risk: safe
source: official
---
```

## Directory Structure

Each skill follows this standard layout:

```
skills/your-skill-name/
├── SKILL.md          # Required: frontmatter + AI agent instructions
├── README.md         # Recommended: human-readable documentation
├── scripts/          # Scripts used by the skill (.py, .js, .sh, .bat)
├── examples/         # Example inputs, outputs, or usage samples
└── references/       # Reference documents or data files
```

- Place all scripts (`.py`, `.js`, `.sh`, `.bat`) inside `scripts/`.
- Place example files and sample data inside `examples/`.
- Place reference documents or supporting data inside `references/`.
- If the skill has a different license than the repository, include a `LICENSE` file in the skill directory.

## Pre-Submission Checklist

Before opening a pull request, verify the following:

- [ ] Skill directory uses kebab-case naming
- [ ] `SKILL.md` exists with valid YAML frontmatter
- [ ] All required frontmatter fields are present and filled in (`name`, `description`, `version`, `author`, `created`, `updated`, `category`, `tags`)
- [ ] The `name` field matches the directory name
- [ ] The `category` field uses one of the valid categories
- [ ] `README.md` is included with overview, prerequisites, usage, and output sections
- [ ] Scripts are placed in the `scripts/` directory
- [ ] Examples are placed in the `examples/` directory
- [ ] No credentials, `.env` files, or sensitive data are included
- [ ] The skill works as described in the SKILL.md workflow
