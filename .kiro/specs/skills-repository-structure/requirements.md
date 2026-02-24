# Requirements Document

## Introduction

This repository is a collection of AI agent skills for multiple platforms (Kiro, GitHub Copilot CLI, Claude Code, Codex). Each skill contains prompts, scripts, and documentation to automate cloud operations and document processing tasks. This document defines the requirements for a standardized repository structure, best practice files, and usage guides so the repository is easy to maintain, contribute to, and use by other developers.

## Glossary

- **Repository**: The git repository storing the entire skills collection
- **Skill**: A single AI agent capability consisting of prompts, scripts, and documentation within one directory
- **SKILL.md**: The primary file of each skill containing YAML frontmatter metadata and complete instructions for the AI agent
- **Frontmatter**: The YAML metadata block at the top of SKILL.md containing name, description, version, author, tags, and other information
- **Skill_Template**: A template directory and file set used as a reference for creating new skills
- **README_Root**: The README.md file at the repository root describing the overall repository
- **CONTRIBUTING_Guide**: The CONTRIBUTING.md file containing guidelines for adding new skills

## Requirements

### Requirement 1: Root Repository README

**User Story:** As a developer, I want a README.md at the repository root that explains the repository purpose, lists available skills, and describes usage, so that I can quickly understand the repository contents.

#### Acceptance Criteria

1. THE README_Root SHALL contain a repository title, short description, and a list of all available skills with a brief description for each
2. THE README_Root SHALL contain a "How to Use" section explaining the steps to use a skill on various platforms (Kiro, GitHub Copilot CLI, Claude Code, Codex)
3. THE README_Root SHALL contain a "Repository Structure" section displaying the tree structure of the repository
4. THE README_Root SHALL contain a "Adding a New Skill" section that references the CONTRIBUTING_Guide
5. THE README_Root SHALL contain license information for the repository

### Requirement 2: Contributing Guide

**User Story:** As a contributor, I want a clear guide for adding new skills, so that I can create skills consistent with the repository standards.

#### Acceptance Criteria

1. THE CONTRIBUTING_Guide SHALL explain the steps to create a new skill from scratch using the Skill_Template
2. THE CONTRIBUTING_Guide SHALL define the naming convention for skill directories using kebab-case format
3. THE CONTRIBUTING_Guide SHALL define the required and optional fields in the SKILL.md Frontmatter
4. THE CONTRIBUTING_Guide SHALL describe the minimal directory structure every skill must have
5. THE CONTRIBUTING_Guide SHALL describe the review process and checklist before adding a skill to the repository

### Requirement 3: Skill Template

**User Story:** As a contributor, I want a ready-to-use skill template, so that I can create new skills quickly and consistently.

#### Acceptance Criteria

1. THE Skill_Template SHALL contain a SKILL.md file with complete Frontmatter including placeholders for all required fields (name, description, version, author, created, updated, category, tags)
2. THE Skill_Template SHALL contain a README.md file with a standard structure (Overview, Prerequisites, Usage, Output)
3. THE Skill_Template SHALL contain an empty `scripts/` directory with a placeholder file
4. THE Skill_Template SHALL contain an empty `examples/` directory with a placeholder file

### Requirement 4: Comprehensive Gitignore

**User Story:** As a developer, I want a .gitignore that covers all file types that should not be tracked, so that the repository stays clean from irrelevant files.

#### Acceptance Criteria

1. THE Repository SHALL have a root .gitignore covering patterns for Python, Node.js, environment files, and common output files
2. WHEN a skill has Node.js dependencies, THE Repository SHALL ignore the `node_modules/` directory within that skill
3. THE Repository SHALL ignore `.env` files, credential files, and temporary output files (JSON scan results, generated documents)

### Requirement 5: Repository License

**User Story:** As a user, I want to know the repository license, so that I understand the rights and restrictions for using the skills.

#### Acceptance Criteria

1. THE Repository SHALL have a LICENSE file at the root defining the license for the entire repository
2. WHERE a skill has a different license from the repository, THE Skill SHALL include its own LICENSE file within the skill directory

### Requirement 6: Consistent Skill Structure

**User Story:** As a repository maintainer, I want every skill to follow a consistent structure, so that the repository is easy to navigate and maintain.

#### Acceptance Criteria

1. THE Repository SHALL require every skill to have at minimum a SKILL.md file with valid Frontmatter
2. THE Frontmatter SHALL contain required fields: name, description, version, author, created, updated, category, tags
3. WHEN a skill has scripts, THE Skill SHALL place all scripts inside a `scripts/` directory
4. WHEN a skill has usage examples, THE Skill SHALL place examples inside an `examples/` directory
