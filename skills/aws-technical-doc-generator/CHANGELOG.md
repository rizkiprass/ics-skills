# Changelog

All notable changes to the AWS Technical Document Generator skill will be documented in this file.

## [2.1.0] - 2026-02-21

### Added
- **DOCX Conversion**: Automatic conversion of Markdown documents to Word (.docx) format
- **docx-js Integration**: Professional Word document generation with proper formatting
- **Dual Format Output**: Generate both .md and .docx files in one command
- **Manual Conversion Script**: `convert-md-to-docx.js` for converting existing Markdown files
- **Node.js Dependencies**: Added package.json with docx package

### Fixed
- **Field Mapping Bug**: Fixed incorrect field names when reading AWS scan data
  - VPC, Subnet, EC2, Security Groups, and IAM sections now populate correctly
  - Added helper methods `get_tag_value()` and `get_instance_specs()`
  - Updated all data access to use correct AWS API field names (PascalCase)
- **Script Generator**: Updated `generate-document-professional.py` with correct field mappings

### Changed
- **Enhanced Workflow**: Added Step 3 (DOCX conversion) to `generate-from-env.py`
- **Documentation**: Updated SKILL.md with DOCX conversion instructions
- **Output Files**: Now generates both .md and .docx formats by default

### Technical Details
- Created `scripts/convert-md-to-docx.js` for Markdown to DOCX conversion
- Created `scripts/fix-document.py` for fixing existing documents with N/A values
- Added `package.json` for Node.js dependency management
- DOCX features: Professional formatting, tables with borders, headers/footers, page numbering

## [2.0.0] - 2026-02-21

### Major Changes
- **Professional Format as Default**: Changed default output format from simple to professional template
- **Output Location**: All generated files now saved to project root directory (not inside skill folder)
- **Renamed Components**: Removed "KCI" branding, using generic "Professional" naming

### Added
- Professional template format with comprehensive sections
- Baseline template in examples folder
- Complete documentation suite
- Support for both Professional and Standard formats

### Changed
- Default format: Professional (was: Standard)
- Output location: Project root (was: Skill folder)
- File naming: Generic professional naming (was: KCI-specific)
- Script names: `generate-document-professional.py` (was: `generate-document-kci-format.py`)

### Removed
- Duplicate documentation files
- Language-specific files (Indonesian versions)
- Unused testing and workflow files
- KCI-specific branding from file names

## [1.0.0] - 2026-02-20

### Initial Release
- AWS resource scanning functionality
- Basic document generation
- Standard format output
- IAM policy templates
- Configuration via .env file

---

## Migration Guide

### From v1.0.0 to v2.0.0

**No breaking changes** - fully backward compatible.

**What changed:**
- Default command now generates Professional format
- Files saved to project root instead of skill folder

**To use Standard format (old behavior):**
```bash
python scripts/generate-from-env-standard.py
```

**To use Professional format (new default):**
```bash
python scripts/generate-from-env.py
```

---

## Format Comparison

| Feature | Standard | Professional |
|---------|----------|--------------|
| Cover Page | ❌ | ✅ |
| Confidentiality | ❌ | ✅ |
| Document Control | Basic | Full |
| Resource Tables | Basic | Comprehensive |
| Security Section | Basic | Detailed |
| Cost Optimization | ❌ | ✅ |
| Tutorials | ❌ | ✅ |

---

**Maintained by**: Cloud Engineering Team  
**Last Updated**: February 21, 2026
