# Skill Name

> Short description of what this skill does.

## Overview

Explain the purpose of this skill, what problem it solves, and the expected outcome. Include context on when and why a user would use this skill.

## Prerequisites

- **Platform**: List the AI platforms this skill supports (e.g., Kiro, Claude Code)
- **Access**: Any required AWS accounts, API keys, or permissions
- **Dependencies**: Any tools, packages, or runtimes that must be installed (e.g., Python 3.10+, Node.js 18+)
- **Input files**: Any files or data the user must provide before running the skill

## Usage

1. Copy the skill directory or reference the `SKILL.md` file from your AI platform.
2. Provide the required inputs as described in the SKILL.md workflow.
3. Run the skill and review the generated output.

```bash
# Example command or invocation (replace with actual usage)
```

## Output

Describe what the skill produces after a successful run:

- **Files**: List any generated files (e.g., `output/report.xlsx`, `output/summary.md`)
- **Format**: Describe the output format and structure
- **Location**: Where the output files are saved

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Skill fails to start | Missing dependencies | Run `pip install -r requirements.txt` or `npm install` |
| Empty output | Invalid or missing input files | Verify input files exist and match the expected format |
| Permission denied | Insufficient AWS credentials | Check IAM permissions and configure credentials |
