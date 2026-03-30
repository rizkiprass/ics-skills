---
name: incident-report
description: >
  Generate professional incident report documents (.docx) from source files.
  Use this skill when the user wants to create an incident report, IR document,
  or post-incident document from a .docx or .txt source file in the project root.
  Triggers include: "incident report", "IR", "create report", "generate report",
  "issue report", or any request to produce an incident report document.
---

# Incident Report Generator

Generate a formatted .docx incident report from a source document (.docx or .txt) in the project root.

## Workflow

1. Identify the source file in the project root (.docx or .txt)
2. Extract content from the source:
   - For .docx: use pandoc to convert to markdown, then read the markdown
   - For .txt: read directly
3. Analyze the extracted content and structure it into the report JSON format
4. Write the JSON data file
5. Run the generator script
6. Clean up temporary files

## Source Content Extraction

For .docx files:
```bash
pandoc "source_file.docx" -o temp_extracted.md
```
Then read temp_extracted.md to get the content.

For .txt files: read the file directly.

## JSON Data Structure

Create a JSON file with this structure, populated from the source content:

```json
{
  "title": "Short incident title",
  "description": "Full incident description paragraph(s)",
  "timeline": [
    { "date": "YYYY-MM-DD", "event": "What happened" }
  ],
  "rootCause": "Root cause analysis text",
  "awsFindings": "AWS support findings if applicable, otherwise general technical findings",
  "evidence": [
    { "caption": "Description of screenshot", "path": "path/to/image.png" }
  ],
  "resolution": "Resolution steps and next actions"
}
```

### Field mapping guidance:
- **title**: Derive a concise title from the main topic of the source
- **description**: Use the main body/overview text from the source
- **timeline**: Extract dates and events mentioned; infer chronological order
- **rootCause**: Identify root cause analysis sections; if not explicit, summarize findings
- **awsFindings**: Extract any AWS support or technical investigation findings
- **evidence**: Include image paths if the source references screenshots (from media/ folder for .docx)
- **resolution**: Extract action items, next steps, or recommendations

If a section has no corresponding content in the source, use a reasonable placeholder like "To be determined" or "Not available".

## Generate the Report

```bash
node .kiro/skills/incident-report/scripts/generate_report.js <output_path> <json_data_path>
```

- `output_path`: where to save the .docx (e.g., `Incident_Report.docx`)
- `json_data_path`: path to the JSON data file

## Report Sections

The generated report includes:
1. **Incident Title** - centered header with date
2. **Incident Description** - overview of the incident
3. **Timeline / Chronology** - formatted table with dates and events
4. **Root Cause Analysis** - analysis of the underlying cause
5. **AWS Support Findings** - technical findings from investigation
6. **Evidence / Screenshots** - embedded images with captions
7. **Resolution / Next Steps** - action items and recommendations

## Dependencies

- Node.js with `docx` package (`npm install docx`)
- pandoc (for .docx source extraction)

## Cleanup

After generating the report, remove temporary files:
- The extracted markdown file (if .docx source)
- The JSON data file
