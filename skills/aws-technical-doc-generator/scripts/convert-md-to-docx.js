#!/usr/bin/env node
/**
 * Convert AWS Technical Document from Markdown to DOCX
 * Uses docx-js library to create professional Word documents
 */

const fs = require('fs');
const path = require('path');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, 
        AlignmentType, HeadingLevel, BorderStyle, WidthType, ShadingType,
        PageBreak, Header, Footer, PageNumber, VerticalAlign } = require('docx');

// Parse markdown file
function parseMarkdown(mdContent) {
    const lines = mdContent.split('\n');
    const sections = [];
    let currentSection = { type: 'root', text: '', content: [] };
    let currentTable = null;
    let inCodeBlock = false;
    let tableCaption = null;
    
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        const trimmedLine = line.trim();
        
        // Skip code blocks
        if (trimmedLine.startsWith('```')) {
            inCodeBlock = !inCodeBlock;
            continue;
        }
        if (inCodeBlock) continue;
        
        // Skip empty lines
        if (trimmedLine === '') {
            // If we have a completed table, add it
            if (currentTable && currentTable.headers.length > 0 && currentTable.rows.length > 0) {
                currentSection.content.push({ 
                    type: 'table', 
                    data: currentTable,
                    caption: tableCaption 
                });
                currentTable = null;
                tableCaption = null;
            }
            continue;
        }
        
        // Heading 1
        if (trimmedLine.startsWith('# ')) {
            if (currentTable && currentTable.headers.length > 0) {
                currentSection.content.push({ 
                    type: 'table', 
                    data: currentTable,
                    caption: tableCaption 
                });
                currentTable = null;
                tableCaption = null;
            }
            if (currentSection && currentSection.type !== 'root') sections.push(currentSection);
            currentSection = { type: 'h1', text: trimmedLine.substring(2), content: [] };
        }
        // Heading 2
        else if (trimmedLine.startsWith('## ')) {
            if (currentTable && currentTable.headers.length > 0) {
                currentSection.content.push({ 
                    type: 'table', 
                    data: currentTable,
                    caption: tableCaption 
                });
                currentTable = null;
                tableCaption = null;
            }
            if (currentSection && currentSection.type !== 'root') sections.push(currentSection);
            currentSection = { type: 'h2', text: trimmedLine.substring(3), content: [] };
        }
        // Heading 3
        else if (trimmedLine.startsWith('### ')) {
            if (currentTable && currentTable.headers.length > 0) {
                currentSection.content.push({ 
                    type: 'table', 
                    data: currentTable,
                    caption: tableCaption 
                });
                currentTable = null;
                tableCaption = null;
            }
            if (currentSection) {
                currentSection.content.push({ type: 'h3', text: trimmedLine.substring(4) });
            }
        }
        // Table caption (italic text before table)
        else if (trimmedLine.startsWith('*Table ') && trimmedLine.endsWith('*')) {
            tableCaption = trimmedLine.substring(1, trimmedLine.length - 1);
        }
        // Bold text (section titles)
        else if (trimmedLine.startsWith('**') && trimmedLine.endsWith('**')) {
            if (currentTable && currentTable.headers.length > 0) {
                currentSection.content.push({ 
                    type: 'table', 
                    data: currentTable,
                    caption: tableCaption 
                });
                currentTable = null;
                tableCaption = null;
            }
            if (currentSection) {
                currentSection.content.push({ type: 'bold', text: trimmedLine.substring(2, trimmedLine.length - 2) });
            }
        }
        // Italic text (figure captions) - but not table captions
        else if (trimmedLine.startsWith('*') && trimmedLine.endsWith('*') && !trimmedLine.startsWith('**') && !trimmedLine.startsWith('*Table ')) {
            if (currentSection) {
                currentSection.content.push({ type: 'italic', text: trimmedLine.substring(1, trimmedLine.length - 1) });
            }
        }
        // Table detection
        else if (trimmedLine.startsWith('| ') && trimmedLine.endsWith(' |')) {
            const cells = trimmedLine.split('|').slice(1, -1).map(c => c.trim());
            
            // Check if this is a separator line
            if (cells.every(cell => cell.match(/^-+$/))) {
                // This is the separator, previous line was headers
                continue;
            }
            
            // Check if next line is separator
            if (i + 1 < lines.length) {
                const nextLine = lines[i + 1].trim();
                if (nextLine.startsWith('|') && nextLine.includes('---')) {
                    // This is the header row
                    if (!currentTable) {
                        currentTable = { headers: [], rows: [] };
                    }
                    currentTable.headers = cells;
                    i++; // Skip separator line
                    continue;
                }
            }
            
            // This is a data row
            if (currentTable && currentTable.headers.length > 0) {
                currentTable.rows.push(cells);
            }
        }
        // Bullet list
        else if (trimmedLine.startsWith('- ')) {
            if (currentTable && currentTable.headers.length > 0) {
                currentSection.content.push({ 
                    type: 'table', 
                    data: currentTable,
                    caption: tableCaption 
                });
                currentTable = null;
                tableCaption = null;
            }
            if (currentSection) {
                currentSection.content.push({ type: 'bullet', text: trimmedLine.substring(2) });
            }
        }
        // Regular paragraph
        else {
            if (currentTable && currentTable.headers.length > 0) {
                currentSection.content.push({ 
                    type: 'table', 
                    data: currentTable,
                    caption: tableCaption 
                });
                currentTable = null;
                tableCaption = null;
            }
            if (currentSection) {
                currentSection.content.push({ type: 'text', text: trimmedLine });
            }
        }
    }
    
    // Add any remaining table
    if (currentTable && currentTable.headers.length > 0 && currentSection) {
        currentSection.content.push({ 
            type: 'table', 
            data: currentTable,
            caption: tableCaption 
        });
    }
    
    if (currentSection && currentSection.type !== 'root') sections.push(currentSection);
    
    return sections;
}

// Create DOCX document
function createDocx(sections) {
    const children = [];
    const border = { style: BorderStyle.SINGLE, size: 1, color: "000000" };
    const borders = { top: border, bottom: border, left: border, right: border };
    
    // Page width calculation (US Letter with 1" margins)
    const pageWidth = 9360; // 12240 - 2880 (margins)
    
    for (const section of sections) {
        // Add heading
        if (section.type === 'h1') {
            children.push(new Paragraph({
                heading: HeadingLevel.HEADING_1,
                children: [new TextRun({ text: section.text, bold: true, size: 32 })],
                spacing: { before: 240, after: 120 }
            }));
        } else if (section.type === 'h2') {
            children.push(new Paragraph({
                heading: HeadingLevel.HEADING_2,
                children: [new TextRun({ text: section.text, bold: true, size: 28 })],
                spacing: { before: 200, after: 100 }
            }));
        }
        
        // Add content
        for (const item of section.content) {
            if (item.type === 'h3') {
                children.push(new Paragraph({
                    heading: HeadingLevel.HEADING_3,
                    children: [new TextRun({ text: item.text, bold: true, size: 24 })],
                    spacing: { before: 160, after: 80 }
                }));
            } else if (item.type === 'bold') {
                children.push(new Paragraph({
                    children: [new TextRun({ text: item.text, bold: true, size: 24 })],
                    spacing: { after: 120 }
                }));
            } else if (item.type === 'italic') {
                children.push(new Paragraph({
                    children: [new TextRun({ text: item.text, italics: true, size: 22 })],
                    alignment: AlignmentType.CENTER,
                    spacing: { after: 120 }
                }));
            } else if (item.type === 'text') {
                children.push(new Paragraph({
                    children: [new TextRun({ text: item.text, size: 22 })],
                    spacing: { after: 100 }
                }));
            } else if (item.type === 'bullet') {
                children.push(new Paragraph({
                    children: [new TextRun({ text: item.text, size: 22 })],
                    bullet: { level: 0 },
                    spacing: { after: 80 }
                }));
            } else if (item.type === 'table') {
                const table = item.data;
                const numCols = table.headers.length;
                const colWidth = Math.floor(pageWidth / numCols);
                const columnWidths = Array(numCols).fill(colWidth);
                
                // Add table caption if exists
                if (item.caption) {
                    children.push(new Paragraph({
                        children: [new TextRun({ text: item.caption, italics: true, size: 20 })],
                        spacing: { before: 120, after: 80 }
                    }));
                }
                
                const rows = [];
                
                // Header row with blue background
                rows.push(new TableRow({
                    children: table.headers.map(header => new TableCell({
                        borders,
                        width: { size: colWidth, type: WidthType.DXA },
                        shading: { fill: "4472C4", type: ShadingType.CLEAR },
                        margins: { top: 100, bottom: 100, left: 150, right: 150 },
                        verticalAlign: VerticalAlign.CENTER,
                        children: [new Paragraph({
                            children: [new TextRun({ text: header, bold: true, color: "FFFFFF", size: 20 })],
                            alignment: AlignmentType.CENTER
                        })]
                    }))
                }));
                
                // Data rows with alternating colors
                for (let rowIdx = 0; rowIdx < table.rows.length; rowIdx++) {
                    const row = table.rows[rowIdx];
                    const bgColor = rowIdx % 2 === 0 ? "FFFFFF" : "F2F2F2";
                    
                    rows.push(new TableRow({
                        children: row.map(cell => new TableCell({
                            borders,
                            width: { size: colWidth, type: WidthType.DXA },
                            shading: { fill: bgColor, type: ShadingType.CLEAR },
                            margins: { top: 80, bottom: 80, left: 120, right: 120 },
                            verticalAlign: VerticalAlign.CENTER,
                            children: [new Paragraph({
                                children: [new TextRun({ text: cell, size: 20 })],
                                alignment: AlignmentType.LEFT
                            })]
                        }))
                    }));
                }
                
                children.push(new Table({
                    width: { size: pageWidth, type: WidthType.DXA },
                    columnWidths,
                    rows
                }));
                
                children.push(new Paragraph({ text: "", spacing: { after: 240 } }));
            }
        }
        
        // Add page break after major sections (except last)
        if (section.type === 'h1' && sections.indexOf(section) < sections.length - 1) {
            children.push(new Paragraph({ children: [new PageBreak()] }));
        }
    }
    
    // Create document
    const doc = new Document({
        styles: {
            default: {
                document: {
                    run: { font: "Arial", size: 22 }
                }
            },
            paragraphStyles: [
                {
                    id: "Heading1",
                    name: "Heading 1",
                    basedOn: "Normal",
                    next: "Normal",
                    quickFormat: true,
                    run: { size: 32, bold: true, font: "Arial", color: "000000" },
                    paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 0 }
                },
                {
                    id: "Heading2",
                    name: "Heading 2",
                    basedOn: "Normal",
                    next: "Normal",
                    quickFormat: true,
                    run: { size: 28, bold: true, font: "Arial", color: "000000" },
                    paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 1 }
                },
                {
                    id: "Heading3",
                    name: "Heading 3",
                    basedOn: "Normal",
                    next: "Normal",
                    quickFormat: true,
                    run: { size: 24, bold: true, font: "Arial", color: "000000" },
                    paragraph: { spacing: { before: 160, after: 80 }, outlineLevel: 2 }
                }
            ]
        },
        sections: [{
            properties: {
                page: {
                    size: {
                        width: 12240,  // 8.5 inches
                        height: 15840  // 11 inches
                    },
                    margin: {
                        top: 1440,    // 1 inch
                        right: 1440,
                        bottom: 1440,
                        left: 1440
                    }
                }
            },
            headers: {
                default: new Header({
                    children: [new Paragraph({
                        children: [new TextRun({
                            text: "AWS Technical Document",
                            size: 20,
                            color: "666666"
                        })],
                        alignment: AlignmentType.RIGHT
                    })]
                })
            },
            footers: {
                default: new Footer({
                    children: [new Paragraph({
                        children: [
                            new TextRun({ text: "Page ", size: 20 }),
                            new TextRun({ children: [PageNumber.CURRENT], size: 20 })
                        ],
                        alignment: AlignmentType.CENTER
                    })]
                })
            },
            children
        }]
    });
    
    return doc;
}

// Main function
async function main() {
    if (process.argv.length < 3) {
        console.error('Usage: node convert-md-to-docx.js <markdown-file>');
        process.exit(1);
    }
    
    const mdFile = process.argv[2];
    const outputFile = mdFile.replace('.md', '.docx');
    
    console.log(`\n📄 Converting ${mdFile} to DOCX...`);
    console.log('=' .repeat(60));
    
    // Read markdown file
    const mdContent = fs.readFileSync(mdFile, 'utf-8');
    
    // Parse markdown
    console.log('📖 Parsing markdown content...');
    const sections = parseMarkdown(mdContent);
    console.log(`✓ Found ${sections.length} sections`);
    
    // Count tables
    let tableCount = 0;
    for (const section of sections) {
        for (const item of section.content) {
            if (item.type === 'table') tableCount++;
        }
    }
    console.log(`✓ Found ${tableCount} tables`);
    
    // Create DOCX
    console.log('📝 Creating DOCX document...');
    const doc = createDocx(sections);
    
    // Save to file
    console.log('💾 Saving document...');
    const buffer = await Packer.toBuffer(doc);
    fs.writeFileSync(outputFile, buffer);
    
    console.log(`✅ Document saved to: ${outputFile}`);
    console.log('=' .repeat(60));
}

main().catch(err => {
    console.error('❌ Error:', err.message);
    process.exit(1);
});
