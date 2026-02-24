# DOCX Conversion Guide

## Overview

The AWS Technical Document Generator now automatically converts Markdown documents to professional Word (.docx) format using the docx-js library.

## Features

- **Automatic Conversion**: Runs automatically after Markdown generation
- **Professional Formatting**: 
  - Arial font throughout
  - Proper heading hierarchy (H1, H2, H3)
  - Tables with borders and blue headers
  - Page headers with document title
  - Page footers with page numbers
  - US Letter page size (8.5" x 11")
  - 1-inch margins on all sides

## Requirements

### Node.js
Version 14 or higher is required. Check your version:
```bash
node --version
```

### Install Dependencies
```bash
cd .kiro/skills/aws-technical-doc-generator
npm install
```

This installs the `docx` package (v8.5.0) required for Word document generation.

## Usage

### Automatic Conversion (Recommended)

When you run the main generation script, DOCX conversion happens automatically:

```bash
python scripts/generate-from-env.py
```

Output:
```
<project-root>/Technical-Document-[Customer]-[Project]-v[Version].md
<project-root>/Technical-Document-[Customer]-[Project]-v[Version].docx
```

### Manual Conversion

To convert an existing Markdown file:

```bash
cd .kiro/skills/aws-technical-doc-generator
node scripts/convert-md-to-docx.js path/to/document.md
```

The DOCX file will be created in the same directory with the same name (but .docx extension).

## Document Structure

The converter handles:

- **Headings**: # (H1), ## (H2), ### (H3)
- **Bold Text**: **text**
- **Italic Text**: *text*
- **Tables**: Markdown tables with headers
- **Bullet Lists**: - item
- **Paragraphs**: Regular text

## Formatting Details

### Tables
- Header row: Blue background (#4472C4) with white text
- Data rows: White background with black text
- All cells: Black borders, proper padding
- Auto-sized columns based on content

### Page Layout
- Size: US Letter (8.5" x 11")
- Margins: 1 inch on all sides
- Header: "AWS Technical Document" (right-aligned, gray)
- Footer: "Page X" (centered)

### Typography
- Font: Arial
- Default size: 11pt
- H1: 16pt bold
- H2: 14pt bold
- H3: 12pt bold
- Table text: 10pt

## Troubleshooting

### "Cannot find module 'docx'"

Install dependencies:
```bash
cd .kiro/skills/aws-technical-doc-generator
npm install
```

### "Node.js not found"

Install Node.js from https://nodejs.org/ (LTS version recommended)

### DOCX file not created

Check the console output for errors. The script will show warnings if:
- Node.js is not installed
- docx package is not installed
- Markdown file is not found

### Tables not rendering correctly

Ensure your Markdown tables have:
- Proper header row
- Separator line with `---`
- Consistent number of columns

Example:
```markdown
| Column 1 | Column 2 |
| --- | --- |
| Data 1 | Data 2 |
```

## Advanced Usage

### Customize Formatting

Edit `scripts/convert-md-to-docx.js` to customize:
- Colors (search for hex codes like `#4472C4`)
- Font sizes (search for `size:` properties)
- Margins (search for `margin:` properties)
- Page size (search for `width:` and `height:`)

### Batch Conversion

Convert multiple files:
```bash
for file in *.md; do
  node scripts/convert-md-to-docx.js "$file"
done
```

## Integration with Other Tools

The DOCX files are compatible with:
- Microsoft Word (2016 and later)
- Google Docs (upload and edit)
- LibreOffice Writer
- Apple Pages
- Online converters (for PDF export)

## Version History

- **v2.1.0** (2026-02-21): Initial DOCX conversion feature
  - Automatic conversion in main workflow
  - Manual conversion script
  - Professional formatting with tables and headers

## Support

For issues or questions:
1. Check this guide
2. Review CHANGELOG.md for recent changes
3. Check SKILL.md for general documentation
4. Review the console output for specific error messages
