# Examples - AWS Technical Document Generator

This folder contains example documents and templates for reference.

## 📄 Available Examples

### 1. Technical-Document-Baseline-KCI-Template.md

**Description**: Baseline template untuk KCI format technical document.

**Purpose**: 
- Reference untuk struktur dokumen KCI
- Contoh format profesional yang lengkap
- Template untuk customization

**Generated From**:
- Customer: PT Telkom Indonesia
- Project: SAP HANA Migration
- Region: ap-southeast-3
- Date: February 21, 2026

**Sections Included**:
- ✅ Cover Page dengan branding profesional
- ✅ Confidentiality Agreement
- ✅ Document Control (version tracking & signatures)
- ✅ Section 1: AWS Solution Overview
- ✅ Section 2: AWS Resource List (comprehensive tables)
- ✅ Section 3: Security
- ✅ Section 4: Cost Optimization
- ✅ Section 5: Tutorial

**Use Cases**:
1. **Reference**: Lihat struktur lengkap dokumen KCI
2. **Customization**: Copy dan modifikasi untuk kebutuhan spesifik
3. **Training**: Pelajari format dokumentasi profesional
4. **Quality Check**: Bandingkan output Anda dengan baseline

## 🎯 How to Use These Examples

### As a Reference

```bash
# View the baseline template
cat .kiro/skills/aws-technical-doc-generator/examples/Technical-Document-Baseline-KCI-Template.md
```

### As a Starting Point

```bash
# Copy template untuk customization
cp .kiro/skills/aws-technical-doc-generator/examples/Technical-Document-Baseline-KCI-Template.md \
   my-custom-template.md

# Edit sesuai kebutuhan
nano my-custom-template.md
```

### For Comparison

Setelah generate dokumen baru, bandingkan dengan baseline:

```bash
# Generate dokumen baru
cd .kiro/skills/aws-technical-doc-generator
python scripts/generate-from-env.py

# Bandingkan dengan baseline
diff <project-root>/Technical-Document-*.md \
     examples/Technical-Document-Baseline-KCI-Template.md
```

## 📊 Document Structure Overview

### Cover Page
- Company branding
- Customer information
- Project name
- Contact details

### Confidentiality Agreement
- Legal protection clause
- Usage restrictions
- Copyright notice

### Document Control
- Version tracking table
- Distribution list
- Document acceptance signatures

### Section 1: AWS Solution Overview
- Architecture diagram placeholder
- AWS services deployed
- Region information

### Section 2: AWS Resource List
- Naming conventions table
- VPC details
- Subnet configuration
- EC2 instances with specifications
- Security groups with rules
- S3 buckets
- CloudWatch alarms
- IAM users

### Section 3: Security
- EBS encryption
- IAM best practices
- CloudTrail configuration

### Section 4: Cost Optimization
- Reserved Instances
- Right sizing recommendations
- Scheduler instances
- Savings Plans
- VPC Endpoints

### Section 5: Tutorial
- Create VPC
- Create Subnet
- Create EC2
- AWS Backup setup
- CloudWatch monitoring

## 💡 Tips for Using Templates

1. **Customize Branding**: Update company information di cover page
2. **Update Contact Info**: Ganti email dan alamat dengan informasi Anda
3. **Add Architecture Diagram**: Replace placeholder dengan diagram aktual
4. **Fill N/A Values**: Lengkapi semua nilai N/A dengan data real
5. **Review Legal Text**: Sesuaikan confidentiality agreement dengan kebutuhan legal Anda
6. **Update Tutorials**: Customize tutorial section sesuai implementasi spesifik

## 🔄 Updating Examples

Jika Anda membuat improvement pada template:

1. Generate dokumen baru dengan improvement
2. Review dan validate
3. Copy ke examples folder dengan nama yang jelas
4. Update README ini dengan informasi template baru

## 📝 Contributing

Jika Anda memiliki contoh dokumen yang bagus:

1. Pastikan tidak ada informasi sensitif (credentials, IP internal, dll)
2. Anonymize customer information jika perlu
3. Add ke folder examples dengan nama deskriptif
4. Update README ini

## 🔒 Security Note

**PENTING**: 
- Jangan commit dokumen dengan informasi sensitif
- Anonymize semua data customer sebelum dijadikan example
- Remove atau mask semua credentials, IP addresses, account IDs
- Review dokumen sebelum share

## 📚 Related Documentation

- **Main README**: `../README.md`
- **KCI Format Guide**: `../README-KCI-FORMAT.md`
- **Quick Start**: `../QUICKSTART.md`
- **How to Use**: `../HOW-TO-USE.md`

---

**Last Updated**: February 21, 2026  
**Maintained By**: Cloud Engineering Team
