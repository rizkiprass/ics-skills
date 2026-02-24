# AI Agent Skills Repository

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A collection of AI agent skills for multiple platforms — Kiro, GitHub Copilot CLI, Claude Code, and Codex. Each skill contains prompts, scripts, and documentation to automate cloud operations and document processing tasks.

## Skills Catalog

| Skill | Description | Category | Platforms |
|-------|-------------|----------|-----------|
| [aws-screener-summary](skills/aws-screener-summary/) | Generate summary reports from AWS Service Screener output, filtered by severity and grouped by Well-Architected pillars | cloud-operations | Kiro, Claude Code |
| [aws-technical-doc-generator](skills/aws-technical-doc-generator/) | Automate creation of comprehensive technical documentation for AWS cloud infrastructure projects | documentation | Kiro, GitHub Copilot CLI, Claude Code, Codex |
| [cloud-sow-analyzer](skills/cloud-sow-analyzer/) | Analyze cloud migration Scope of Work (SOW) documents to identify risks, issues, and recommendations | cloud-architecture | GitHub Copilot CLI, Claude Code, Codex |
| [docx](skills/docx/) | Create, read, edit, and manipulate Word documents (.docx files) | document-processing | Kiro, GitHub Copilot CLI, Claude Code, Codex |

## How to Use

Each skill is self-contained in its own directory under `skills/`. The `SKILL.md` file is the primary file — it contains the AI agent instructions and metadata. Choose the section below that matches your platform.

### Kiro

1. Copy the skill's `SKILL.md` file into your project's `.kiro/skills/` directory:
   ```bash
   mkdir -p .kiro/skills/
   cp skills/<skill-name>/SKILL.md .kiro/skills/<skill-name>.md
   ```
2. Kiro will automatically detect the skill and use it when relevant prompts are triggered.
3. If the skill has scripts, copy the `scripts/` directory into your project as well:
   ```bash
   cp -r skills/<skill-name>/scripts/ .kiro/skills/<skill-name>/scripts/
   ```

### GitHub Copilot CLI

1. Open the skill's `SKILL.md` file and copy the content (excluding the YAML frontmatter).
2. Paste the instructions into your Copilot CLI prompt or custom instructions file.
3. Install any dependencies listed in the skill's `README.md`.
4. Run the skill workflow as described in the `SKILL.md`.

### Claude Code

1. Copy the skill's `SKILL.md` content into your Claude Code project instructions or `CLAUDE.md` file:
   ```bash
   cat skills/<skill-name>/SKILL.md >> CLAUDE.md
   ```
2. Claude Code will follow the instructions when you reference the skill's capabilities.
3. Ensure any required scripts and dependencies are available in your project.

### Codex

1. Include the skill's `SKILL.md` content in your Codex system prompt or project instructions.
2. Reference the skill's workflow steps when prompting Codex.
3. Make sure any scripts the skill depends on are accessible in the working directory.

## Repository Structure

```
skills-repo/
├── README.md                    # Repository overview and usage guide
├── CONTRIBUTING.md              # Guide for adding new skills
├── LICENSE                      # MIT License
├── .gitignore                   # Comprehensive ignore rules
├── _template/                   # Skill template for new skills
│   ├── SKILL.md
│   ├── README.md
│   ├── scripts/
│   └── examples/
└── skills/
    ├── aws-screener-summary/
    ├── aws-technical-doc-generator/
    ├── cloud-sow-analyzer/
    └── docx/
```

## Adding a New Skill

1. Copy the `_template/` directory to `skills/your-skill-name/`.
2. Fill in the `SKILL.md` frontmatter and write the AI agent instructions.
3. Add a `README.md` with human-readable documentation.
4. Run through the pre-submission checklist.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide, naming conventions, frontmatter spec, and review checklist.

## License

This repository is licensed under the [MIT License](LICENSE). Individual skills may have their own license — check the skill directory for a `LICENSE` file if one exists.
