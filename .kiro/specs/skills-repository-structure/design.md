# Design Document: Skills Repository Structure

## Overview

This design defines the standardized structure, best practice files, and conventions for a git repository that hosts a collection of AI agent skills. The repository targets multiple AI platforms (Kiro, GitHub Copilot CLI, Claude Code, Codex) and primarily contains Python and Node.js-based skills focused on AWS cloud operations and document processing.

The design establishes:
- A root-level file set (README.md, CONTRIBUTING.md, LICENSE, .gitignore)
- A skill template for consistent skill creation
- Conventions for skill directory layout and metadata

## Architecture

The repository follows a flat collection pattern where each skill is a self-contained directory under `skills/`.

```
skills-repo/
├── README.md                    # Repository overview and usage guide
├── CONTRIBUTING.md              # Guide for adding new skills
├── LICENSE                      # Repository-wide license (MIT)
├── .gitignore                   # Comprehensive ignore rules
├── _template/                   # Skill template for new skills
│   ├── SKILL.md
│   ├── README.md
│   ├── scripts/
│   │   └── .gitkeep
│   └── examples/
│       └── .gitkeep
└── skills/
    ├── aws-screener-summary/
    ├── aws-technical-doc-generator/
    ├── cloud-sow-analyzer/
    └── docx/
```

Key design decisions:
- **Flat skill directory**: All skills live directly under `skills/` with no nested categories. This keeps navigation simple and avoids premature categorization. Tags in SKILL.md frontmatter handle categorization.
- **`_template/` at root**: The template lives at the root (not inside `skills/`) to distinguish it from actual skills. The underscore prefix makes it sort first and signals it's not a real skill.
- **Self-contained skills**: Each skill directory contains everything needed to use that skill, including its own dependencies, scripts, and documentation.

## Components and Interfaces

### Component 1: README.md (Root)

The root README serves as the entry point for the repository.

Sections:
1. **Header**: Repository name, one-line description, badges (license)
2. **Skills Catalog**: Table listing each skill with name, description, category, and platforms
3. **How to Use**: Platform-specific instructions for Kiro, GitHub Copilot CLI, Claude Code, and Codex
4. **Repository Structure**: Tree view of the repository layout
5. **Adding a New Skill**: Brief instructions with link to CONTRIBUTING.md
6. **License**: License statement

The skills catalog table format:

| Skill | Description | Category | Platforms |
|-------|-------------|----------|-----------|
| [aws-screener-summary](skills/aws-screener-summary/) | Generate summary reports from AWS Service Screener output | cloud-operations | Kiro, Claude Code |
| ... | ... | ... | ... |

### Component 2: CONTRIBUTING.md

The contributing guide defines the process and standards for adding new skills.

Sections:
1. **Quick Start**: Copy `_template/`, rename, fill in SKILL.md
2. **Naming Convention**: kebab-case directory names, descriptive and concise
3. **Required Files**: SKILL.md (mandatory), README.md (recommended)
4. **SKILL.md Frontmatter Spec**: Required and optional fields with types and examples
5. **Directory Structure**: Standard layout with `scripts/`, `examples/`, `references/`
6. **Checklist**: Pre-submission checklist for quality

Required frontmatter fields:
```yaml
---
name: skill-name              # string, kebab-case, matches directory name
description: "..."            # string, trigger description for AI agent
version: 1.0.0               # string, semver format
author: Team Name             # string
created: 2026-01-01           # date, ISO format
updated: 2026-01-01           # date, ISO format
category: cloud-operations    # string, one of predefined categories
tags: [aws, documentation]    # array of strings
---
```

Optional frontmatter fields:
```yaml
platforms: [kiro, claude-code]  # array, target AI platforms
license: MIT                    # string, if different from repo
risk: safe                      # string: safe | moderate | dangerous
source: community               # string: community | official
```

### Component 3: Skill Template (`_template/`)

A copy-ready template directory containing:

- **SKILL.md**: Frontmatter with placeholder values + standard section structure (Overview, Workflow, Notes)
- **README.md**: Human-readable documentation template (Overview, Prerequisites, Usage, Output, Troubleshooting)
- **scripts/.gitkeep**: Empty directory placeholder
- **examples/.gitkeep**: Empty directory placeholder

### Component 4: .gitignore (Updated)

The existing .gitignore is Python-focused. It needs additions for:
- `node_modules/` (already partially covered by skill-level .gitignore)
- Common output files: `*.xlsx`, `*.docx` (generated outputs)
- Scan result files: `*-scan-results.json`, `aws-resources-*.json`
- OS files: `.DS_Store`, `Thumbs.db`
- Editor files: `.vscode/`, `.idea/`

### Component 5: LICENSE

MIT License file at the repository root. This matches the existing license used by `aws-technical-doc-generator` and `cloud-sow-analyzer`.

## Data Models

### SKILL.md Frontmatter Schema

```yaml
# Required fields
name: string          # kebab-case, must match directory name
description: string   # AI agent trigger description
version: string       # semver (e.g., "1.0.0")
author: string        # author or team name
created: date         # ISO date (YYYY-MM-DD)
updated: date         # ISO date (YYYY-MM-DD)
category: string      # predefined category
tags: string[]        # array of lowercase tags

# Optional fields
platforms: string[]   # target AI platforms
license: string       # skill-specific license
risk: string          # safe | moderate | dangerous
source: string        # community | official
```

Valid categories: `cloud-operations`, `documentation`, `cloud-architecture`, `document-processing`, `devops`, `security`

Valid platforms: `kiro`, `github-copilot-cli`, `claude-code`, `codex`


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system — essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

Property 1: README skill catalog completeness
*For any* set of skill directories under `skills/`, the README.md skills catalog table SHALL contain an entry for every skill directory.
**Validates: Requirements 1.1**

Property 2: Template frontmatter completeness
*For any* set of required frontmatter fields (name, description, version, author, created, updated, category, tags), the `_template/SKILL.md` file SHALL contain a placeholder for each field.
**Validates: Requirements 3.1**

Property 3: Gitignore pattern coverage
*For any* file matching a known ignorable pattern (Python bytecode, node_modules, .env, generated output files), the root .gitignore SHALL match that file path.
**Validates: Requirements 4.1, 4.2, 4.3**

Property 4: Skill-specific license presence
*For any* skill whose frontmatter `license` field differs from the repository license, that skill directory SHALL contain its own LICENSE file.
**Validates: Requirements 5.2**

Property 5: Skill frontmatter validity
*For any* skill directory under `skills/`, the directory SHALL contain a SKILL.md file with valid YAML frontmatter that includes all required fields (name, description, version, author, created, updated, category, tags).
**Validates: Requirements 6.1, 6.2**

Property 6: Skill directory structure compliance
*For any* skill directory, script files (`.py`, `.js`, `.sh`, `.bat`) SHALL be located inside a `scripts/` subdirectory, and example/sample files SHALL be located inside an `examples/` subdirectory.
**Validates: Requirements 6.3, 6.4**

## Error Handling

Since this feature is about repository structure and static files (not runtime code), error handling focuses on validation scenarios:

1. **Missing SKILL.md**: If a directory under `skills/` lacks a SKILL.md file, the contributing checklist should catch this during review.
2. **Invalid Frontmatter**: If SKILL.md frontmatter is missing required fields or has invalid YAML, contributors should be guided by the template and checklist.
3. **Naming Mismatch**: If the `name` field in frontmatter doesn't match the directory name, the checklist should flag this.
4. **Missing Template Files**: If `_template/` is accidentally deleted or modified, the CONTRIBUTING.md still documents the required structure independently.

## Testing Strategy

### Unit Tests (Example-Based)
- Verify README.md contains expected section headings ("How to Use", "Repository Structure", "Adding a New Skill")
- Verify CONTRIBUTING.md contains expected section headings and references to the template
- Verify `_template/` directory contains SKILL.md, README.md, scripts/.gitkeep, examples/.gitkeep
- Verify LICENSE file exists at root

### Property-Based Tests
- **Property 1**: Generate random sets of skill directory names, verify README catalog lists all of them
- **Property 2**: Generate random subsets of required fields, verify template SKILL.md contains all of them
- **Property 3**: Generate random file paths matching ignorable patterns, verify .gitignore matches them
- **Property 5**: For all existing skill directories, parse SKILL.md frontmatter and verify required fields
- **Property 6**: For all existing skill directories, verify script and example files are in correct subdirectories

### Testing Library
- Use `pytest` with `hypothesis` for property-based testing (Python is the primary language in this repository)
- Minimum 100 iterations per property test
- Each test tagged with: **Feature: skills-repository-structure, Property {number}: {property_text}**
