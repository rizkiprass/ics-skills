# Implementation Plan: Skills Repository Structure

## Overview

Create the standardized repository structure, best practice files, and skill template for the AI agent skills collection repository. All files are static documentation and configuration — no runtime code. Implementation uses existing repository content to populate the skills catalog and ensure consistency.

## Tasks

- [x] 1. Create root-level best practice files
  - [x] 1.1 Create LICENSE file at repository root
    - Use MIT License with current year
    - _Requirements: 5.1_
  - [x] 1.2 Update .gitignore with comprehensive patterns
    - Add Node.js patterns (node_modules/)
    - Add OS files (.DS_Store, Thumbs.db)
    - Add editor files (.vscode/, .idea/)
    - Add generated output files (*.xlsx, *.docx in root)
    - Add scan result patterns (*-scan-results.json, aws-resources-*.json)
    - Keep all existing Python patterns
    - _Requirements: 4.1, 4.2, 4.3_

- [x] 2. Create skill template
  - [x] 2.1 Create `_template/SKILL.md` with frontmatter placeholders
    - Include all required fields: name, description, version, author, created, updated, category, tags
    - Include optional fields: platforms, license, risk, source
    - Include standard sections: Overview, Workflow, Notes
    - _Requirements: 3.1, 6.2_
  - [x] 2.2 Create `_template/README.md` with standard structure
    - Include sections: Overview, Prerequisites, Usage, Output, Troubleshooting
    - _Requirements: 3.2_
  - [x] 2.3 Create `_template/scripts/.gitkeep` and `_template/examples/.gitkeep`
    - Empty placeholder files to preserve directory structure in git
    - _Requirements: 3.3, 3.4_

- [x] 3. Create CONTRIBUTING.md
  - [x] 3.1 Write CONTRIBUTING.md with complete contributor guide
    - Quick start steps using _template/
    - Naming convention (kebab-case)
    - Required and optional frontmatter fields with types and examples
    - Minimal directory structure description
    - Pre-submission checklist
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

- [x] 4. Create README.md
  - [x] 4.1 Write root README.md with all required sections
    - Repository title, description, and license badge
    - Skills catalog table (populated from existing skills: aws-screener-summary, aws-technical-doc-generator, cloud-sow-analyzer, docx)
    - How to Use section with platform-specific instructions (Kiro, GitHub Copilot CLI, Claude Code, Codex)
    - Repository Structure tree view
    - Adding a New Skill section referencing CONTRIBUTING.md
    - License section
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

- [x] 5. Checkpoint - Review all files
  - Ensure all files are created and consistent with each other
  - Verify cross-references (README links to CONTRIBUTING, CONTRIBUTING references _template/)
  - Ensure all tests pass, ask the user if questions arise.

- [ ]* 5.1 Write property tests for repository structure validation
    - **Property 5: Skill frontmatter validity**
    - **Validates: Requirements 6.1, 6.2**

- [ ]* 5.2 Write property test for skill directory structure compliance
    - **Property 6: Skill directory structure compliance**
    - **Validates: Requirements 6.3, 6.4**

- [x] 6. Final checkpoint - Ensure all files are complete
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- All documentation is written in English per user preference
- The skills catalog in README.md is populated from the 4 existing skills
- Property tests use pytest + hypothesis
