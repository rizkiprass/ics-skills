#!/usr/bin/env node
/**
 * Validate Markdown to DOCX conversion
 * Shows statistics about parsed content
 */

const fs = require('fs');

function parseMarkdown(mdContent) {
    const lines = mdContent.split('\n');
    const stats = {
        sections: 0,
        h1: 0,
        h2: 0,
        h3: 0,
        tables: 0,
        tableRows: 0,
        paragraphs: 0,
        bullets: 0
    };
    
    let currentTable = null;
    let inCodeBlock = false;
    
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        const trimmedLine = line.trim();
        
        if (trimmedLine.startsWith('```')) {
            inCodeBlock = !inCodeBlock;
            continue;
        }
        if (inCodeBlock) continue;
        if (trimmedLine === '') continue;
        
        if (trimmedLine.startsWith('# ')) {
            stats.h1++;
            stats.sections++;
            if (currentTable) {
                stats.tables++;
                stats.tableRows += currentTable.rows;
                currentTable = null;
            }
        } else if (trimmedLine.startsWith('## ')) {
            stats.h2++;
            stats.sections++;
            if (currentTable) {
                stats.tables++;
                stats.tableRows += currentTable.rows;
                currentTable = null;
            }
        } else if (trimmedLine.startsWith('### ')) {
            stats.h3++;
        } else if (trimmedLine.startsWith('| ') && trimmedLine.endsWith(' |')) {
            const cells = trimmedLine.split('|').slice(1, -1).map(c => c.trim());
            
            if (cells.every(cell => cell.match(/^-+$/))) {
                continue;
            }
            
            if (i + 1 < lines.length) {
                const nextLine = lines[i + 1].trim();
                if (nextLine.startsWith('|') && nextLine.includes('---')) {
                    if (!currentTable) {
                        currentTable = { rows: 0 };
                    }
                    i++;
                    continue;
                }
            }
            
            if (currentTable) {
                currentTable.rows++;
            }
        } else if (trimmedLine.startsWith('- ')) {
            stats.bullets++;
            if (currentTable) {
                stats.tables++;
                stats.tableRows += currentTable.rows;
                currentTable = null;
            }
        } else if (!trimmedLine.startsWith('*')) {
            stats.paragraphs++;
            if (currentTable) {
                stats.tables++;
                stats.tableRows += currentTable.rows;
                currentTable = null;
            }
        }
    }
    
    if (currentTable) {
        stats.tables++;
        stats.tableRows += currentTable.rows;
    }
    
    return stats;
}

function main() {
    if (process.argv.length < 3) {
        console.error('Usage: node validate-conversion.js <markdown-file>');
        process.exit(1);
    }
    
    const mdFile = process.argv[2];
    
    console.log('\n📊 Markdown Conversion Validation');
    console.log('='.repeat(60));
    console.log(`File: ${mdFile}\n`);
    
    const mdContent = fs.readFileSync(mdFile, 'utf-8');
    const stats = parseMarkdown(mdContent);
    
    console.log('Content Statistics:');
    console.log(`  Sections: ${stats.sections} (H1: ${stats.h1}, H2: ${stats.h2}, H3: ${stats.h3})`);
    console.log(`  Tables: ${stats.tables} (${stats.tableRows} total rows)`);
    console.log(`  Paragraphs: ${stats.paragraphs}`);
    console.log(`  Bullet points: ${stats.bullets}`);
    console.log('\n' + '='.repeat(60));
    
    if (stats.tables === 0) {
        console.log('⚠️  WARNING: No tables detected!');
        console.log('Check if tables are properly formatted with | separators');
    } else {
        console.log(`✅ ${stats.tables} tables detected and ready for conversion`);
    }
    console.log();
}

main();
