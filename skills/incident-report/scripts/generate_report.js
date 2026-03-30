/**
 * Incident Report Generator
 * 
 * Usage: node generate_report.js <output_path> <json_data_path>
 * 
 * json_data_path should point to a JSON file with this structure:
 * {
 *   "title": "Incident Title",
 *   "description": "Incident description text...",
 *   "timeline": [
 *     { "date": "2026-03-09", "event": "Issue first reported" },
 *     ...
 *   ],
 *   "rootCause": "Root cause analysis text...",
 *   "awsFindings": "AWS support findings text...",
 *   "evidence": [
 *     { "caption": "Screenshot description", "path": "path/to/image.png" }
 *   ],
 *   "resolution": "Resolution and next steps text..."
 * }
 */

const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  ImageRun, Header, Footer, AlignmentType, HeadingLevel, BorderStyle,
  WidthType, ShadingType, PageNumber, PageBreak, LevelFormat
} = require("docx");

const args = process.argv.slice(2);
if (args.length < 2) {
  console.error("Usage: node generate_report.js <output_path> <json_data_path>");
  process.exit(1);
}

const outputPath = args[0];
const dataPath = args[1];
const data = JSON.parse(fs.readFileSync(dataPath, "utf-8"));

// Colors
const PRIMARY = "1F4E79";
const ACCENT = "2E75B6";
const LIGHT_BG = "D6E4F0";
const BORDER_COLOR = "B4C6E7";
const WHITE = "FFFFFF";

const border = { style: BorderStyle.SINGLE, size: 1, color: BORDER_COLOR };
const borders = { top: border, bottom: border, left: border, right: border };
const cellMargins = { top: 80, bottom: 80, left: 120, right: 120 };

// Helper: create a section heading
function sectionHeading(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 360, after: 200 },
    children: [new TextRun({ text, bold: true, font: "Arial", size: 28, color: PRIMARY })]
  });
}

// Helper: body paragraph
function bodyParagraph(text) {
  return new Paragraph({
    spacing: { after: 120 },
    children: [new TextRun({ text, font: "Arial", size: 22 })]
  });
}

// Helper: multi-line text to paragraphs
function textToParagraphs(text) {
  if (!text) return [bodyParagraph("")];
  return text.split("\n").filter(l => l.trim()).map(l => bodyParagraph(l.trim()));
}

// Build title section
function buildTitle(title) {
  return [
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 600, after: 100 },
      children: [new TextRun({ text: "INCIDENT REPORT", bold: true, font: "Arial", size: 40, color: PRIMARY })]
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 100 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: ACCENT } },
      children: [new TextRun({ text: title || "Untitled Incident", font: "Arial", size: 28, color: ACCENT })]
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 400 },
      children: [new TextRun({ text: `Date: ${new Date().toISOString().split("T")[0]}`, font: "Arial", size: 20, color: "666666" })]
    })
  ];
}

// Build timeline table
function buildTimeline(timeline) {
  if (!timeline || timeline.length === 0) {
    return [sectionHeading("Timeline / Chronology"), bodyParagraph("No timeline data provided.")];
  }
  const headerRow = new TableRow({
    tableHeader: true,
    children: [
      new TableCell({
        borders, width: { size: 2500, type: WidthType.DXA },
        shading: { fill: PRIMARY, type: ShadingType.CLEAR },
        margins: cellMargins,
        children: [new Paragraph({ children: [new TextRun({ text: "Date", bold: true, font: "Arial", size: 20, color: WHITE })] })]
      }),
      new TableCell({
        borders, width: { size: 6860, type: WidthType.DXA },
        shading: { fill: PRIMARY, type: ShadingType.CLEAR },
        margins: cellMargins,
        children: [new Paragraph({ children: [new TextRun({ text: "Event", bold: true, font: "Arial", size: 20, color: WHITE })] })]
      })
    ]
  });

  const rows = timeline.map((item, i) => new TableRow({
    children: [
      new TableCell({
        borders, width: { size: 2500, type: WidthType.DXA },
        shading: { fill: i % 2 === 0 ? LIGHT_BG : WHITE, type: ShadingType.CLEAR },
        margins: cellMargins,
        children: [new Paragraph({ children: [new TextRun({ text: item.date || "", font: "Arial", size: 20 })] })]
      }),
      new TableCell({
        borders, width: { size: 6860, type: WidthType.DXA },
        shading: { fill: i % 2 === 0 ? LIGHT_BG : WHITE, type: ShadingType.CLEAR },
        margins: cellMargins,
        children: [new Paragraph({ children: [new TextRun({ text: item.event || "", font: "Arial", size: 20 })] })]
      })
    ]
  }));

  return [
    sectionHeading("Timeline / Chronology"),
    new Table({
      width: { size: 9360, type: WidthType.DXA },
      columnWidths: [2500, 6860],
      rows: [headerRow, ...rows]
    })
  ];
}

// Build evidence section with images
function buildEvidence(evidence) {
  if (!evidence || evidence.length === 0) {
    return [sectionHeading("Evidence / Screenshots"), bodyParagraph("No evidence provided.")];
  }
  const items = [];
  items.push(sectionHeading("Evidence / Screenshots"));
  for (const item of evidence) {
    if (item.path && fs.existsSync(item.path)) {
      const ext = path.extname(item.path).slice(1).toLowerCase() || "png";
      const imgType = ext === "jpg" ? "jpeg" : ext;
      const imgData = fs.readFileSync(item.path);
      items.push(new Paragraph({
        spacing: { before: 200, after: 80 },
        children: [new ImageRun({
          type: imgType,
          data: imgData,
          transformation: { width: 580, height: 380 },
          altText: { title: item.caption || "Evidence", description: item.caption || "Evidence screenshot", name: "evidence" }
        })]
      }));
    }
    if (item.caption) {
      items.push(new Paragraph({
        spacing: { after: 200 },
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: item.caption, font: "Arial", size: 18, italics: true, color: "666666" })]
      }));
    }
  }
  return items;
}

// Assemble document
const children = [
  ...buildTitle(data.title),
  sectionHeading("Incident Description"),
  ...textToParagraphs(data.description),
  ...buildTimeline(data.timeline),
  sectionHeading("Root Cause Analysis"),
  ...textToParagraphs(data.rootCause),
  sectionHeading("AWS Support Findings"),
  ...textToParagraphs(data.awsFindings),
  ...buildEvidence(data.evidence),
  sectionHeading("Resolution / Next Steps"),
  ...textToParagraphs(data.resolution)
];

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      {
        id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial", color: PRIMARY },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 }
      }
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          alignment: AlignmentType.RIGHT,
          children: [new TextRun({ text: "Incident Report", font: "Arial", size: 16, color: "999999", italics: true })]
        })]
      })
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "Page ", font: "Arial", size: 16, color: "999999" }),
            new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 16, color: "999999" })
          ]
        })]
      })
    },
    children
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(outputPath, buffer);
  console.log(`Report generated: ${outputPath}`);
}).catch(err => {
  console.error("Error generating report:", err);
  process.exit(1);
});
