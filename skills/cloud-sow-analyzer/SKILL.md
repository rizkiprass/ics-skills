---
name: cloud-sow-analyzer
description: "Analyzes cloud migration Scope of Work (SOW) documents to identify risks, issues, and provide recommendations for AWS migration projects"
version: 1.0.0
author: Cloud Architecture Team
created: 2026-02-21
updated: 2026-02-21
platforms: [github-copilot-cli, claude-code, codex]
category: cloud-architecture
tags: [cloud-migration, aws, risk-assessment, sow-analysis]
risk: safe
source: community
---

# cloud-sow-analyzer

## Purpose

Skill ini membantu Cloud Architect menganalisis dokumen Scope of Work (SOW) untuk proyek cloud migration dan implementation. Skill akan membaca file DOCX yang berisi executive summary, success criteria, objective migration, implementation plan, architecture, resource list, dan calculator resources, kemudian menghasilkan analisis komprehensif dalam format markdown dengan fokus pada risk assessment dan discovery issue.

## When to Use This Skill

Gunakan skill ini ketika:
- Anda menerima dokumen SOW baru untuk proyek cloud migration
- Perlu melakukan risk assessment sebelum memulai migration
- Ingin mengidentifikasi potensi masalah di awal proyek
- Membutuhkan analisis terstruktur dari dokumen SOW
- Perlu validasi kelengkapan informasi dalam SOW

## Core Capabilities

1. **SOW Document Analysis** - Membaca dan mengekstrak informasi dari file DOCX
2. **Interactive Clarification** - Menanyakan informasi yang kurang sebelum generate output
3. **Risk Assessment** - Mengidentifikasi risiko untuk migration dan implementation
4. **Issue Discovery** - Menemukan potensi masalah berdasarkan SOW content
5. **Recommendation Generation** - Memberikan rekomendasi actionable
6. **Markdown Report** - Menghasilkan laporan terstruktur dalam format .md

## Supported Cloud Providers

- Amazon Web Services (AWS)


## Main Workflow

### Phase 1: Document Input & Initial Validation

**Step 1: Receive SOW Document**

Terima file DOCX dari user dan lakukan validasi awal:

```bash
# Check if file exists and is readable
if [[ ! -f "$SOW_FILE" ]]; then
    echo "❌ Error: File not found: $SOW_FILE"
    exit 1
fi

# Check file extension
if [[ ! "$SOW_FILE" =~ \.docx$ ]]; then
    echo "⚠️  Warning: File is not .docx format. Attempting to process..."
fi
```

**Step 2: Extract Content**

Ekstrak konten dari DOCX menggunakan tools yang tersedia:

```bash
# Option 1: Using pandoc (recommended)
pandoc "$SOW_FILE" -t markdown -o temp_sow.md

# Option 2: Using python-docx
python3 << EOF
from docx import Document
doc = Document('$SOW_FILE')
for para in doc.paragraphs:
    print(para.text)
EOF
```

**Step 3: Identify SOW Sections**

Identifikasi section-section utama dalam dokumen:
- Executive Summary
- Success Criteria
- Migration Objectives
- Implementation Plan
- Architecture Design
- Resource List (to be deployed/migrated)
- Resource Calculator/Sizing

### Phase 2: Interactive Clarification

Sebelum melakukan analisis, tanyakan informasi yang mungkin kurang atau perlu klarifikasi:

**Ask the user:**

1. **Cloud Provider Confirmation**
   ```
   Dari dokumen SOW, cloud provider yang terdeteksi: AWS
   Apakah ini sudah benar? [Y/n]
   ```

2. **Migration Type**
   ```
   Jenis migration yang akan dilakukan:
   [ ] Lift & Shift (Rehost)
   [ ] Replatform
   [ ] Refactor/Re-architect
   [ ] Hybrid (kombinasi)
   [ ] Tidak disebutkan dalam SOW
   ```

3. **Timeline Information**
   ```
   Apakah timeline migration sudah jelas dalam SOW?
   - Start Date: [dari SOW atau tanyakan]
   - Target Completion: [dari SOW atau tanyakan]
   - Phase breakdown: [ada/tidak ada]
   ```

4. **Current Environment**
   ```
   Informasi environment saat ini:
   - On-premise / Cloud lain / Hybrid?
   - Jumlah aplikasi yang akan di-migrate: [dari SOW]
   - Kompleksitas: [Low/Medium/High]
   ```

5. **Compliance & Security Requirements**
   ```
   Apakah ada requirement khusus untuk:
   - Compliance (ISO, PCI-DSS, GDPR, dll)?
   - Data residency?
   - Security standards?
   ```

6. **Budget Information**
   ```
   Apakah budget/cost estimation sudah ada dalam SOW?
   - Budget range: [dari SOW atau tanyakan]
   - Cost optimization priority: [High/Medium/Low]
   ```


### Phase 3: Risk Assessment Analysis

Lakukan analisis risiko berdasarkan informasi dari SOW dan jawaban user:

**Risk Categories to Assess:**

1. **Technical Risks**
   - Architecture complexity
   - Technology compatibility
   - Data migration challenges
   - Integration points
   - Performance requirements
   - Scalability concerns

2. **Operational Risks**
   - Team skill gaps
   - Resource availability
   - Timeline feasibility
   - Change management
   - Rollback strategy
   - Business continuity

3. **Security & Compliance Risks**
   - Data protection
   - Access control
   - Compliance requirements
   - Audit trails
   - Encryption requirements
   - Network security

4. **Financial Risks**
   - Cost overrun potential
   - Hidden costs
   - Resource sizing accuracy
   - Licensing issues
   - Ongoing operational costs

5. **Vendor/Provider Risks**
   - Service availability
   - Support coverage
   - Regional limitations
   - Service maturity
   - Lock-in concerns

**Risk Scoring Matrix:**

```
Risk Level = Probability × Impact

Probability:
- Low (1): < 25% chance
- Medium (2): 25-50% chance
- High (3): 50-75% chance
- Critical (4): > 75% chance

Impact:
- Low (1): Minor delays, < 10% budget impact
- Medium (2): Moderate delays, 10-25% budget impact
- High (3): Significant delays, 25-50% budget impact
- Critical (4): Project failure risk, > 50% budget impact

Risk Score:
- 1-4: Low Risk (Green)
- 5-8: Medium Risk (Yellow)
- 9-12: High Risk (Orange)
- 13-16: Critical Risk (Red)
```

### Phase 4: Issue Discovery

Identifikasi potensi masalah berdasarkan analisis SOW:

**Common Issues to Check:**

1. **SOW Completeness Issues**
   - Missing architecture diagrams
   - Unclear success criteria
   - Incomplete resource inventory
   - Vague timeline
   - Missing dependencies
   - No rollback plan

2. **Technical Issues**
   - Incompatible services between providers
   - Network bandwidth limitations
   - Data transfer size concerns
   - Application dependencies not mapped
   - Legacy system integration challenges

3. **Resource Planning Issues**
   - Under/over-sized resources
   - Missing disaster recovery plan
   - No backup strategy
   - Insufficient monitoring plan
   - Missing cost optimization strategy

4. **Process Issues**
   - No testing strategy
   - Missing validation criteria
   - Unclear roles and responsibilities
   - No communication plan
   - Missing training plan


### Phase 5: Generate Markdown Report

Buat laporan komprehensif dalam format markdown dengan struktur berikut:

**Output File Structure:**

```markdown
# Cloud Migration SOW Analysis Report

**Project:** [Project Name from SOW]
**Cloud Provider:** [AWS]
**Analysis Date:** [Current Date]
**Analyzed By:** [User Name]

---

## 1. Executive Summary

### 1.1 Project Overview
[Ringkasan dari SOW executive summary]

### 1.2 Key Findings
- Total Risks Identified: [Number]
- Critical Risks: [Number]
- High Priority Issues: [Number]
- Overall Risk Level: [Low/Medium/High/Critical]

### 1.3 Recommendation Summary
[Top 3-5 rekomendasi paling penting]

---

## 2. SOW Analysis

### 2.1 Document Completeness
| Section | Status | Completeness | Notes |
|---------|--------|--------------|-------|
| Executive Summary | ✅/⚠️/❌ | [%] | [Comments] |
| Success Criteria | ✅/⚠️/❌ | [%] | [Comments] |
| Migration Objectives | ✅/⚠️/❌ | [%] | [Comments] |
| Implementation Plan | ✅/⚠️/❌ | [%] | [Comments] |
| Architecture Design | ✅/⚠️/❌ | [%] | [Comments] |
| Resource List | ✅/⚠️/❌ | [%] | [Comments] |
| Resource Calculator | ✅/⚠️/❌ | [%] | [Comments] |

**Legend:**
- ✅ Complete and detailed
- ⚠️ Present but needs improvement
- ❌ Missing or insufficient

### 2.2 Success Criteria Analysis
[Analisis dari success criteria yang didefinisikan]

### 2.3 Migration Objectives Validation
[Validasi apakah objectives realistic dan measurable]

---

## 3. Risk Assessment

### 3.1 Risk Summary Dashboard

```
┌─────────────────────────────────────────┐
│        RISK DISTRIBUTION                │
├─────────────────────────────────────────┤
│ 🔴 Critical: [X] risks                  │
│ 🟠 High:     [X] risks                  │
│ 🟡 Medium:   [X] risks                  │
│ 🟢 Low:      [X] risks                  │
├─────────────────────────────────────────┤
│ Total Risks: [X]                        │
└─────────────────────────────────────────┘
```

### 3.2 Detailed Risk Analysis

#### 3.2.1 Technical Risks

| ID | Risk Description | Probability | Impact | Score | Level | Mitigation |
|----|------------------|-------------|--------|-------|-------|------------|
| T-01 | [Description] | [1-4] | [1-4] | [Score] | [Level] | [Mitigation strategy] |
| T-02 | [Description] | [1-4] | [1-4] | [Score] | [Level] | [Mitigation strategy] |

#### 3.2.2 Operational Risks

| ID | Risk Description | Probability | Impact | Score | Level | Mitigation |
|----|------------------|-------------|--------|-------|-------|------------|
| O-01 | [Description] | [1-4] | [1-4] | [Score] | [Level] | [Mitigation strategy] |

#### 3.2.3 Security & Compliance Risks

| ID | Risk Description | Probability | Impact | Score | Level | Mitigation |
|----|------------------|-------------|--------|-------|-------|------------|
| S-01 | [Description] | [1-4] | [1-4] | [Score] | [Level] | [Mitigation strategy] |

#### 3.2.4 Financial Risks

| ID | Risk Description | Probability | Impact | Score | Level | Mitigation |
|----|------------------|-------------|--------|-------|-------|------------|
| F-01 | [Description] | [1-4] | [1-4] | [Score] | [Level] | [Mitigation strategy] |

#### 3.2.5 Vendor/Provider Risks

| ID | Risk Description | Probability | Impact | Score | Level | Mitigation |
|----|------------------|-------------|--------|-------|-------|------------|
| V-01 | [Description] | [1-4] | [1-4] | [Score] | [Level] | [Mitigation strategy] |

---

## 4. Issues & Findings

### 4.1 Critical Issues (Must Fix Before Starting)

1. **[Issue Title]**
   - **Category:** [Technical/Operational/Security/Financial]
   - **Description:** [Detailed description]
   - **Impact:** [What happens if not addressed]
   - **Recommendation:** [How to fix]
   - **Priority:** 🔴 Critical

### 4.2 High Priority Issues (Fix During Planning)

1. **[Issue Title]**
   - **Category:** [Category]
   - **Description:** [Description]
   - **Impact:** [Impact]
   - **Recommendation:** [Recommendation]
   - **Priority:** 🟠 High

### 4.3 Medium Priority Issues (Monitor During Execution)

1. **[Issue Title]**
   - **Category:** [Category]
   - **Description:** [Description]
   - **Impact:** [Impact]
   - **Recommendation:** [Recommendation]
   - **Priority:** 🟡 Medium

### 4.4 Low Priority Issues (Nice to Have)

1. **[Issue Title]**
   - **Category:** [Category]
   - **Description:** [Description]
   - **Impact:** [Impact]
   - **Recommendation:** [Recommendation]
   - **Priority:** 🟢 Low

---

## 5. Architecture Analysis

### 5.1 Current Architecture Assessment
[Analisis architecture saat ini dari SOW]

### 5.2 Target Architecture Review
[Review target architecture yang diusulkan]

### 5.3 Architecture Gaps
[Gap antara current dan target]

### 5.4 Architecture Recommendations
[Rekomendasi improvement untuk architecture]

---

## 6. Resource Analysis

### 6.1 Resource Inventory Review

| Resource Type | Quantity | Sizing | Status | Notes |
|---------------|----------|--------|--------|-------|
| Compute | [X] | [Size] | ✅/⚠️/❌ | [Comments] |
| Storage | [X] | [Size] | ✅/⚠️/❌ | [Comments] |
| Database | [X] | [Size] | ✅/⚠️/❌ | [Comments] |
| Network | [X] | [Size] | ✅/⚠️/❌ | [Comments] |

### 6.2 Resource Sizing Validation
[Validasi apakah sizing sudah appropriate]

### 6.3 Cost Estimation Review
[Review cost calculator dari SOW]

### 6.4 Cost Optimization Opportunities
[Identifikasi peluang untuk optimize cost]

---

## 7. Implementation Plan Analysis

### 7.1 Timeline Feasibility
[Analisis apakah timeline realistic]

### 7.2 Phase Breakdown Review
[Review phase-phase migration]

### 7.3 Dependencies & Prerequisites
[Identifikasi dependencies yang perlu diperhatikan]

### 7.4 Testing Strategy
[Review testing plan dari SOW]

### 7.5 Rollback Strategy
[Review rollback plan]

---

## 8. Recommendations

### 8.1 Immediate Actions (Before Project Start)

1. **[Action Item]**
   - **Why:** [Justification]
   - **How:** [Implementation steps]
   - **Owner:** [Suggested owner]
   - **Timeline:** [Timeframe]

### 8.2 Planning Phase Actions

1. **[Action Item]**
   - **Why:** [Justification]
   - **How:** [Implementation steps]
   - **Owner:** [Suggested owner]
   - **Timeline:** [Timeframe]

### 8.3 Execution Phase Actions

1. **[Action Item]**
   - **Why:** [Justification]
   - **How:** [Implementation steps]
   - **Owner:** [Suggested owner]
   - **Timeline:** [Timeframe]

### 8.4 Post-Migration Actions

1. **[Action Item]**
   - **Why:** [Justification]
   - **How:** [Implementation steps]
   - **Owner:** [Suggested owner]
   - **Timeline:** [Timeframe]

---

## 9. Checklist for Discovery Phase

### 9.1 Pre-Migration Checklist

- [ ] Complete inventory of all resources
- [ ] Network topology documented
- [ ] Dependencies mapped
- [ ] Security requirements validated
- [ ] Compliance requirements confirmed
- [ ] Backup strategy defined
- [ ] Disaster recovery plan created
- [ ] Testing strategy approved
- [ ] Rollback plan documented
- [ ] Team training completed

### 9.2 Migration Readiness Checklist

- [ ] All critical issues resolved
- [ ] High priority issues addressed
- [ ] Architecture validated
- [ ] Resource sizing confirmed
- [ ] Cost estimation approved
- [ ] Timeline agreed upon
- [ ] Stakeholders aligned
- [ ] Communication plan in place
- [ ] Monitoring tools ready
- [ ] Support plan established

---

## 10. Appendix

### 10.1 Cloud Provider Specific Considerations

#### AWS Specific
[AWS-specific considerations dan best practices]

### 10.2 Reference Documents
- Original SOW: [filename]
- Analysis Date: [date]
- Analyst: [name]

### 10.3 Glossary
[Definisi terms yang digunakan dalam report]

---

**Report Generated:** [Timestamp]
**Tool:** cloud-sow-analyzer v1.0.0
```


### Phase 6: Review & Refinement

Setelah generate report, lakukan review dengan user:

**Ask the user:**

```
📊 Analysis report telah dibuat!

Apakah Anda ingin:
1. Review report sekarang
2. Tambahkan analisis untuk area tertentu
3. Export ke format lain (PDF, HTML)
4. Selesai

Pilihan Anda: [1-4]
```

**If user chooses option 2:**
- Tanyakan area mana yang perlu analisis lebih detail
- Generate additional analysis
- Append ke report

**If user chooses option 3:**
```bash
# Convert to PDF using pandoc
pandoc analysis-report.md -o analysis-report.pdf \
  --pdf-engine=xelatex \
  --toc \
  --number-sections

# Convert to HTML
pandoc analysis-report.md -o analysis-report.html \
  --standalone \
  --toc \
  --css=style.css
```

## Cloud Provider Specific Analysis

### AWS Specific Checks

**Service Availability:**
- Check if all required AWS services are available in target region
- Validate service limits and quotas
- Review AWS Well-Architected Framework alignment

**Common AWS Migration Patterns:**
- Database Migration Service (DMS) usage
- Server Migration Service (SMS) for VMs
- DataSync for large data transfers
- Application Migration Service (MGN)

**AWS Best Practices to Validate:**
- Multi-AZ deployment for high availability
- VPC design and subnet strategy
- IAM roles and policies
- CloudWatch monitoring setup
- Cost allocation tags
- Backup using AWS Backup
- Security groups and NACLs

**AWS-Specific Risks:**
- Region-specific service limitations
- Data transfer costs
- EBS vs EFS vs S3 storage decisions
- RDS vs self-managed database
- Lambda cold start issues
- API Gateway throttling

## Error Handling

### Document Processing Errors

**If DOCX cannot be read:**
```
❌ Error: Unable to read DOCX file

Possible solutions:
1. Check if file is corrupted
2. Try converting to PDF first, then extract text
3. Manually copy content to text file
4. Use alternative document format (PDF, TXT)

Would you like to:
- Try alternative extraction method
- Provide content manually
- Exit and fix file
```

**If content extraction is incomplete:**
```
⚠️  Warning: Some sections may not have been extracted properly

Detected sections: [list]
Missing sections: [list]

Would you like to:
1. Proceed with available content
2. Manually provide missing sections
3. Try different extraction method
```

### Analysis Errors

**If critical information is missing:**
```
⚠️  Critical Information Missing

The following information is required for proper analysis:
- [Missing item 1]
- [Missing item 2]

Cannot proceed without this information.

Please provide:
1. Update SOW document
2. Provide information manually
3. Skip this analysis (not recommended)
```

**If risk assessment cannot be completed:**
```
⚠️  Insufficient information for complete risk assessment

Available information: [X%]
Missing information: [list]

Options:
1. Proceed with partial analysis (will be marked as incomplete)
2. Gather missing information first
3. Use assumptions (will be documented)
```

## Usage Examples

### Example 1: Basic SOW Analysis

```bash
# User provides SOW file
$ analyze-sow migration-project-sow.docx

# Skill extracts content and asks clarifications
? Cloud Provider detected: AWS. Is this correct? (Y/n): Y
? Migration Type: 
  [x] Lift & Shift
  [ ] Replatform
  [ ] Refactor
? Timeline Start Date: 2026-03-01
? Timeline End Date: 2026-08-31

# Skill generates analysis
✅ Analysis complete!
📄 Report saved to: migration-project-analysis.md

Summary:
- Total Risks: 15
- Critical: 2
- High: 5
- Medium: 6
- Low: 2

Top 3 Recommendations:
1. Define rollback strategy (Critical)
2. Complete dependency mapping (High)
3. Validate resource sizing (High)
```

### Example 2: Incremental Analysis

```bash
$ analyze-sow project-sow.docx --interactive

# After initial analysis
? Would you like additional analysis? (Y/n): Y
? Select area for deep dive:
  [x] Security & Compliance
  [ ] Cost Optimization
  [ ] Performance

# Generates additional security analysis
✅ Security deep-dive complete!
📄 Appended to: project-analysis.md
```

## Integration with Other Tools

### Integration with AWS Tools

```bash
# Export resource list for AWS Application Discovery Service
$ analyze-sow project-sow.docx --export-aws-discovery

# Generate CloudFormation template from resource list
$ analyze-sow project-sow.docx --generate-cfn-template

# Create AWS Migration Hub import file
$ analyze-sow project-sow.docx --export-migration-hub
```

### Integration with Project Management Tools

```bash
# Export issues to Jira
$ analyze-sow project-sow.docx --export-jira

# Export to Trello board
$ analyze-sow project-sow.docx --export-trello

# Generate MS Project timeline
$ analyze-sow project-sow.docx --export-msproject
```

## Quality Standards

**Analysis Completeness:**
- All SOW sections reviewed: 100%
- Risk assessment coverage: 100%
- Minimum 10 risks identified
- Minimum 5 recommendations provided
- All critical issues documented

**Report Quality:**
- Clear and actionable recommendations
- Risk scores properly calculated
- Mitigation strategies provided
- Timeline realistic
- Cost implications considered

**Validation Checks:**
- SOW completeness validated
- Architecture feasibility checked
- Resource sizing reviewed
- Timeline feasibility assessed
- Budget alignment verified

## Advanced Features

### AI-Powered Analysis

Jika tersedia, gunakan AI untuk:
- Pattern recognition dari SOW sebelumnya
- Prediksi risiko berdasarkan historical data
- Rekomendasi otomatis berdasarkan best practices
- Cost optimization suggestions

### Comparative Analysis

```bash
# Compare with previous SOW versions
$ analyze-sow new-sow.docx --compare-with old-sow.docx

# Compare with industry benchmarks
$ analyze-sow project-sow.docx --benchmark
```

### Automated Monitoring

```bash
# Set up monitoring for SOW changes
$ analyze-sow project-sow.docx --watch

# Get alerts when SOW is updated
$ analyze-sow project-sow.docx --alert-on-change
```

## Best Practices

**Before Analysis:**
1. Ensure SOW document is complete
2. Have access to additional documentation if needed
3. Understand project context
4. Know stakeholder expectations

**During Analysis:**
1. Ask clarifying questions
2. Don't make assumptions without documenting
3. Focus on actionable insights
4. Prioritize critical issues
5. Be realistic in risk assessment

**After Analysis:**
1. Review report with stakeholders
2. Update based on feedback
3. Track issue resolution
4. Monitor risk mitigation progress
5. Update analysis as project evolves

## Maintenance & Updates

**Regular Updates:**
- Update cloud provider service lists quarterly
- Review risk assessment criteria annually
- Update best practices based on lessons learned
- Incorporate new migration patterns

**Version Control:**
- Track analysis versions
- Document changes between versions
- Maintain audit trail
- Archive old analyses

## References

- **AWS Migration Hub:** https://aws.amazon.com/migration-hub/
- **AWS Well-Architected Framework:** https://aws.amazon.com/architecture/well-architected/
- **Cloud Migration Best Practices:** Industry standards and frameworks
- **Risk Assessment Frameworks:** NIST, ISO 27001, COBIT

## Support & Troubleshooting

**Common Issues:**

1. **DOCX extraction fails**
   - Solution: Use alternative extraction method or convert to PDF

2. **Incomplete analysis**
   - Solution: Provide missing information manually

3. **Risk scores seem incorrect**
   - Solution: Review probability and impact assessments

4. **Report too long**
   - Solution: Use summary mode or focus on specific areas

**Getting Help:**
- Check documentation in references/ folder
- Review examples/ for sample analyses
- Contact skill maintainer for support

## License & Attribution

This skill is provided as-is for cloud migration analysis purposes. Users are responsible for validating all analysis results and recommendations before implementation.

**Disclaimer:** This skill provides analysis and recommendations based on the information provided. Always validate findings with cloud provider documentation and consult with certified cloud architects for critical decisions.

