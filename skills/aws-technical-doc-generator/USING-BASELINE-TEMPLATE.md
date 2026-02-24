# Using the Baseline Template

## Overview

The baseline template (`examples/Technical-Document-Baseline-KCI-Template.md`) is a complete, real-world example of a KCI format technical document. It was generated from an actual AWS environment and serves as the gold standard for document structure and formatting.

## What is the Baseline Template?

The baseline template is:
- ✅ A complete KCI format document with all sections
- ✅ Generated from real AWS resources (PT Telkom Indonesia - SAP HANA Migration)
- ✅ Includes actual data examples (anonymized where necessary)
- ✅ Follows professional documentation standards
- ✅ Ready to use as a reference or starting point

## Use Cases

### 1. As a Reference Guide

**When to use**: You want to see what a complete KCI document looks like.

```bash
# View the baseline template
cat .kiro/skills/aws-technical-doc-generator/examples/Technical-Document-Baseline-KCI-Template.md

# Or open in your editor
code .kiro/skills/aws-technical-doc-generator/examples/Technical-Document-Baseline-KCI-Template.md
```

**What to look for**:
- Document structure and section organization
- Table formatting and layout
- Professional language and tone
- How to present AWS resources
- Security and cost optimization sections

### 2. As a Quality Check

**When to use**: After generating a new document, compare it with the baseline.

```bash
# Generate your document
cd .kiro/skills/aws-technical-doc-generator
python scripts/generate-from-env.py

# Compare with baseline
diff <project-root>/Technical-Document-YourCustomer-YourProject-v1.0-KCI.md \
     examples/Technical-Document-Baseline-KCI-Template.md
```

**What to check**:
- Are all sections present?
- Is the formatting consistent?
- Are tables properly structured?
- Is the professional tone maintained?

### 3. As a Customization Starting Point

**When to use**: You need a custom template with specific modifications.

```bash
# Copy baseline to your project
cp .kiro/skills/aws-technical-doc-generator/examples/Technical-Document-Baseline-KCI-Template.md \
   my-custom-template.md

# Customize as needed
nano my-custom-template.md
```

**Common customizations**:
- Update company branding and contact information
- Add custom sections specific to your organization
- Modify legal text (confidentiality agreement)
- Add additional tutorial sections
- Change table structures

### 4. For Training and Onboarding

**When to use**: Training new team members on documentation standards.

**Training activities**:
1. **Review Session**: Walk through the baseline template section by section
2. **Structure Analysis**: Identify key components and their purposes
3. **Comparison Exercise**: Compare baseline with other documents
4. **Customization Practice**: Create a modified version for a fictional project

## Key Sections Explained

### Cover Page
```markdown
**Technical Document**
**PT. Innovation Cloud Services - PT Telkom Indonesia**
SAP HANA Migration
```

**Purpose**: Professional first impression with clear project identification.

**Customization**: Update company names, project name, contact details.

### Confidentiality Agreement
```markdown
# Confidentiality Agreement

The information in this document shall not be disclosed...
```

**Purpose**: Legal protection for sensitive information.

**Customization**: Adjust legal language to match your organization's requirements. Consult legal team if needed.

### Document Control
```markdown
## Document Information
| Client | : | PT Telkom Indonesia |
| Project Name | : | SAP HANA Migration |
```

**Purpose**: Version tracking, distribution list, and approval signatures.

**Customization**: Update version numbers, dates, and stakeholder names.

### Section 2: AWS Resource List

This is the core technical content with comprehensive tables:

**2.1 Naming Conventions**
- Shows standard naming patterns
- Helps maintain consistency

**2.2-2.9 Resource Tables**
- VPC, Subnets, EC2, Security Groups, etc.
- Detailed specifications and configurations

**Customization**: Tables are auto-generated from AWS scan, but you can add custom columns or notes.

### Section 3: Security

Best practices and security configurations:
- EBS encryption
- IAM policies
- CloudTrail setup

**Customization**: Add organization-specific security requirements.

### Section 4: Cost Optimization

Recommendations for cost savings:
- Reserved Instances
- Right sizing
- Savings Plans

**Customization**: Add actual cost analysis from your AWS Cost Explorer.

### Section 5: Tutorial

Step-by-step implementation guides:
- Creating VPC
- Launching EC2
- Setting up monitoring

**Customization**: Add tutorials specific to your implementation.

## Customization Best Practices

### 1. Maintain Structure

✅ **DO**: Keep the section numbering and hierarchy
```markdown
# Section 1: AWS Solution Overview
## 1.1 AWS Architecture Diagram
```

❌ **DON'T**: Change section numbers arbitrarily
```markdown
# Section 1: Overview
## 1.5 Diagram  # Skipped 1.2, 1.3, 1.4
```

### 2. Preserve Table Formatting

✅ **DO**: Keep table structure consistent
```markdown
| No | Name | Value |
| --- | --- | --- |
| 1 | Item | Data |
```

❌ **DON'T**: Break table alignment
```markdown
| No | Name | Value |
|---|---|---|
| 1 | Item | Data |  # Inconsistent separator
```

### 3. Update All Placeholders

✅ **DO**: Replace all N/A values with actual data
```markdown
| VPC ID | vpc-0463b48d377921144 |
```

❌ **DON'T**: Leave N/A in final document
```markdown
| VPC ID | N/A |  # Should be filled
```

### 4. Maintain Professional Tone

✅ **DO**: Use formal, technical language
```markdown
The infrastructure was provisioned in AWS region ap-southeast-3...
```

❌ **DON'T**: Use casual language
```markdown
We set up some stuff in AWS...
```

## Integration with Generator

The baseline template represents the ideal output of the KCI format generator. When you run:

```bash
python scripts/generate-from-env.py
```

The generator aims to produce a document that matches the baseline template's structure and quality.

**Generator → Baseline Relationship**:
1. Generator scans your AWS resources
2. Populates the KCI template structure
3. Produces output similar to baseline
4. You can compare output with baseline for quality check

## Updating the Baseline

If you make improvements to the template structure:

1. **Generate improved document**
   ```bash
   python scripts/generate-from-env.py
   ```

2. **Review and validate**
   - Check all sections are complete
   - Verify formatting is correct
   - Ensure professional quality

3. **Update baseline**
   ```bash
   cp <project-root>/Technical-Document-Improved-v2.0-KCI.md \
      .kiro/skills/aws-technical-doc-generator/examples/Technical-Document-Baseline-KCI-Template-v2.md
   ```

4. **Document changes**
   - Update `examples/README.md`
   - Note what changed and why
   - Update version number

## Common Questions

### Q: Can I modify the baseline template directly?

**A**: Yes, but it's better to copy it first:
```bash
cp examples/Technical-Document-Baseline-KCI-Template.md my-template.md
# Then modify my-template.md
```

### Q: Should I commit my customized template to Git?

**A**: Yes, if it's a reusable template for your organization. But ensure:
- No sensitive data (credentials, internal IPs)
- Customer information is anonymized
- Legal text is reviewed

### Q: How often should the baseline be updated?

**A**: Update when:
- AWS introduces new services you want to document
- You improve the document structure
- You add new sections or best practices
- Feedback suggests improvements

### Q: Can I use the baseline for non-AWS projects?

**A**: The structure can be adapted, but:
- Remove AWS-specific sections
- Update terminology
- Adjust resource tables
- Keep the professional structure

## Tips for Success

1. **Start with the baseline**: Don't reinvent the wheel
2. **Customize incrementally**: Make small changes and test
3. **Get feedback**: Share with team before finalizing
4. **Document changes**: Keep track of customizations
5. **Version control**: Use Git to track template evolution
6. **Review regularly**: Update baseline as standards evolve

## Related Documentation

- **Examples README**: `examples/README.md`
- **KCI Format Guide**: `README-KCI-FORMAT.md`
- **Main README**: `README.md`
- **Quick Start**: `QUICKSTART.md`

---

**Last Updated**: February 21, 2026  
**Version**: 1.0
