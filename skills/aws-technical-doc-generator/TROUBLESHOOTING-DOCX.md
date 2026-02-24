# DOCX Conversion Troubleshooting Guide

## Common Issues and Solutions

### Issue: Tables Not Appearing in DOCX

**Symptoms:**
- DOCX file is created but tables are missing or appear as plain text
- Table data appears jumbled or unformatted

**Causes:**
1. Markdown table format is incorrect
2. Parser not detecting table boundaries
3. Table caption interfering with detection

**Solutions:**

1. **Verify Markdown Table Format**
   
   Correct format:
   ```markdown
   | Column 1 | Column 2 | Column 3 |
   | --- | --- | --- |
   | Data 1 | Data 2 | Data 3 |
   | Data 4 | Data 5 | Data 6 |
   ```
   
   Requirements:
   - Must start and end with `|`
   - Header row followed by separator row with `---`
   - Consistent number of columns in all rows
   - Spaces around `|` are optional but recommended

2. **Check for Empty Lines**
   
   Tables should have empty lines before and after:
   ```markdown
   Some text here.
   
   | Header 1 | Header 2 |
   | --- | --- |
   | Data 1 | Data 2 |
   
   More text here.
   ```

3. **Table Captions**
   
   Italic text before tables is treated as caption:
   ```markdown
   *Table 1. VPC Resources*
   
   | No | Name | VPC ID |
   | --- | --- | --- |
   | 1 | vpc-1 | vpc-123 |
   ```

### Issue: File Locked Error (EBUSY)

**Symptoms:**
```
Error: EBUSY: resource busy or locked
```

**Cause:**
The DOCX file is currently open in Word or another application.

**Solution:**
1. Close the DOCX file in all applications
2. Wait a few seconds for the file handle to release
3. Run the conversion again

Alternative:
```bash
# Convert to a different filename
node scripts/convert-md-to-docx.js document.md
# This creates document-new.docx instead
```

### Issue: Tables Have Wrong Number of Columns

**Symptoms:**
- Some table rows have more/fewer cells than headers
- Table appears misaligned in Word

**Cause:**
Inconsistent number of `|` separators in table rows.

**Solution:**
Ensure all rows have the same number of columns:

```markdown
# ❌ WRONG - inconsistent columns
| A | B | C |
| --- | --- | --- |
| 1 | 2 |        ← Missing column
| 3 | 4 | 5 | 6 | ← Extra column

# ✅ CORRECT - consistent columns
| A | B | C |
| --- | --- | --- |
| 1 | 2 | 3 |
| 4 | 5 | 6 |
```

### Issue: Special Characters Not Displaying

**Symptoms:**
- Characters like `<`, `>`, `&` appear incorrectly
- Unicode characters are garbled

**Cause:**
Special characters need proper encoding in DOCX.

**Solution:**
The converter handles most special characters automatically. If issues persist:
1. Use HTML entities in Markdown: `&lt;`, `&gt;`, `&amp;`
2. Avoid using raw HTML in Markdown tables

### Issue: Table Formatting Looks Different

**Symptoms:**
- Colors don't match expectations
- Borders are missing or wrong style
- Cell padding is too small/large

**Cause:**
Default formatting in the converter.

**Solution:**
Edit `scripts/convert-md-to-docx.js`:

```javascript
// Change header background color (line ~180)
shading: { fill: "4472C4", type: ShadingType.CLEAR },
// Change to: fill: "YOUR_HEX_COLOR"

// Change alternating row colors (line ~195)
const bgColor = rowIdx % 2 === 0 ? "FFFFFF" : "F2F2F2";
// Modify colors as needed

// Change cell padding (line ~200)
margins: { top: 80, bottom: 80, left: 120, right: 120 },
// Adjust values (in twentieths of a point)
```

## Validation Tools

### Check Table Detection

Before converting, validate your Markdown:

```bash
node scripts/validate-conversion.js document.md
```

This shows:
- Number of sections (H1, H2, H3)
- Number of tables detected
- Total table rows
- Paragraphs and bullet points

### Manual Table Count

Count tables in your Markdown:
```bash
# Windows PowerShell
(Get-Content document.md | Select-String "^\| .* \|$").Count / 2
```

Divide by 2 because each table has a header and separator line.

## Best Practices

### 1. Test with Small Documents First

Before converting large documents:
```bash
# Extract first 100 lines for testing
head -n 100 document.md > test.md
node scripts/convert-md-to-docx.js test.md
```

### 2. Use Consistent Formatting

- Always use the same table style throughout
- Keep column widths reasonable (avoid very long text in single cells)
- Use consistent heading levels

### 3. Preview Before Sharing

After conversion:
1. Open DOCX in Word
2. Check all tables are present
3. Verify formatting is correct
4. Check page breaks are appropriate
5. Review headers and footers

### 4. Keep Backups

Always keep the original Markdown file:
```bash
# Create backup before conversion
cp document.md document.md.backup
node scripts/convert-md-to-docx.js document.md
```

## Performance Tips

### Large Documents

For documents with many tables (>50):
- Conversion may take 10-30 seconds
- Memory usage can reach 500MB
- Consider splitting into multiple documents

### Optimization

If conversion is slow:
1. Remove unnecessary empty lines
2. Simplify complex tables
3. Reduce number of columns where possible

## Getting Help

### Debug Mode

Add console.log statements to see what's being parsed:

```javascript
// In convert-md-to-docx.js, after parsing
console.log('Sections:', sections.length);
sections.forEach((s, i) => {
    const tables = s.content.filter(c => c.type === 'table').length;
    console.log(`Section ${i}: ${s.text} - ${tables} tables`);
});
```

### Report Issues

When reporting issues, include:
1. Sample of problematic Markdown (5-10 lines)
2. Expected output description
3. Actual output description
4. Console output from conversion
5. Node.js version (`node --version`)
6. docx package version (`npm list docx`)

## Version Compatibility

### Tested Versions
- Node.js: 14.x, 16.x, 18.x, 20.x
- docx: 8.5.0
- Windows: 10, 11
- Word: 2016, 2019, 2021, 365

### Known Limitations
- Very wide tables (>10 columns) may overflow page width
- Nested tables are not supported
- Images in tables are not supported
- Merged cells are not supported

## Quick Reference

### Markdown Table Syntax
```markdown
| Header 1 | Header 2 | Header 3 |
| --- | --- | --- |
| Cell 1 | Cell 2 | Cell 3 |
| Cell 4 | Cell 5 | Cell 6 |
```

### Conversion Command
```bash
node scripts/convert-md-to-docx.js input.md
# Creates: input.docx
```

### Validation Command
```bash
node scripts/validate-conversion.js input.md
# Shows: statistics about content
```

### Full Workflow
```bash
# 1. Validate
node scripts/validate-conversion.js document.md

# 2. Convert
node scripts/convert-md-to-docx.js document.md

# 3. Verify output exists
ls -l document.docx

# 4. Open in Word for review
start document.docx  # Windows
```
