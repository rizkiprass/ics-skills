# AWS Technical Document Generator

Automate the creation of comprehensive technical documentation for AWS cloud infrastructure projects.

## 🎯 Quick Start

```bash
cd .kiro/skills/aws-technical-doc-generator
pip install -r requirements.txt
cp .env.example .env
# Edit .env dengan AWS credentials Anda
python scripts/generate-from-env.py
```

## 📋 Format Dokumentasi

### ⭐ Default: Professional Format - RECOMMENDED

Format profesional dengan struktur lengkap untuk client-facing documentation.

**Output**: `Technical-Document-[Customer]-[Project]-v[Version].md`

**Mencakup:**
- ✅ Cover page profesional dengan branding
- ✅ Confidentiality agreement
- ✅ Document control & version tracking
- ✅ Comprehensive resource tables
- ✅ Security best practices
- ✅ Cost optimization recommendations
- ✅ Step-by-step tutorials

**Command:**
```bash
python scripts/generate-from-env.py
```

### Alternative: Standard Format (Simple)

Format sederhana untuk dokumentasi internal.

**Output**: `Technical-Document-[Customer]-[Project]-v[Version]-Standard.md`

**Command:**
```bash
python scripts/generate-from-env-standard.py
```

## 📚 Dokumentasi Lengkap

- **Quick Start**: [QUICKSTART.md](QUICKSTART.md) - Panduan 5 menit
- **How to Use**: [HOW-TO-USE.md](HOW-TO-USE.md) - Panduan lengkap
- **Quick Reference**: [QUICK-REFERENCE.md](QUICK-REFERENCE.md) - Command cheat sheet
- **Using Baseline Template**: [USING-BASELINE-TEMPLATE.md](USING-BASELINE-TEMPLATE.md) - Panduan menggunakan template baseline
- **Examples**: [examples/README.md](examples/README.md) - Baseline template & contoh dokumen
- **Changelog**: [CHANGELOG.md](CHANGELOG.md) - Perubahan terbaru

## 🔧 Konfigurasi

Edit file `.env`:

```bash
# AWS Credentials (READ-ONLY recommended)
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=ap-southeast-3

# Project Information
PROJECT_NAME=SAP HANA Migration
CUSTOMER_NAME=PT Telkom Indonesia
DOCUMENT_VERSION=1.0
```

**PENTING**: 
- File `.env` sudah ada di `.gitignore` - tidak akan ter-commit ke Git
- Gunakan `.env.example` sebagai template
- Jangan share file `.env` via email/chat

## 📂 Output Location

Semua file output disimpan di **root directory project** (bukan di folder skill):

```
<project-root>/
├── aws-resources-YYYYMMDD-HHMMSS.json          # Scan results
├── Technical-Document-[...].md                 # Professional format (default)
└── Technical-Document-[...]-Standard.md        # Standard format
```

## 🚀 Features

- ✅ Automatic AWS resource scanning
- ✅ Professional document generation
- ✅ Multiple format support (Professional & Standard)
- ✅ Comprehensive resource tables
- ✅ Security best practices
- ✅ Cost optimization recommendations
- ✅ Step-by-step tutorials
- ✅ Clean output management

## 📊 What Gets Scanned

- **VPC & Networking**: VPC, Subnets, Route Tables, Internet Gateway, NAT Gateway
- **Compute**: EC2 Instances, EBS Volumes
- **Load Balancers**: ALB, NLB
- **Databases**: RDS Instances
- **Storage**: S3 Buckets
- **Security**: Security Groups, IAM Users
- **Monitoring**: CloudWatch Alarms
- **Auto Scaling**: Auto Scaling Groups

## 🔒 Security Best Practices

- **Never commit AWS credentials** to version control
- **Use read-only IAM policies** to prevent accidental modifications
- **Rotate access keys regularly** for security
- **Review generated documents** before sharing
- **Use temporary credentials** when possible (STS assume role)

### Required IAM Permissions

Template IAM policy tersedia di `references/iam-policy-template.json`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:Describe*",
        "elasticloadbalancing:Describe*",
        "rds:Describe*",
        "s3:List*",
        "vpc:Describe*",
        "iam:List*",
        "cloudwatch:Describe*"
      ],
      "Resource": "*"
    }
  ]
}
```

## 💡 Tips

1. **Review sebelum delivery**: Periksa dokumen dan isi nilai N/A dengan data aktual
2. **Tambahkan diagram**: Template menyediakan placeholder untuk architecture diagram
3. **Customize tutorials**: Sesuaikan section tutorial dengan implementasi spesifik Anda
4. **Update branding**: Modifikasi informasi company di script jika perlu

## 🆕 What's New (v2.0.0)

- ✅ **Professional Format sekarang menjadi default**
- ✅ Format Standard tetap tersedia sebagai alternatif
- ✅ Dokumentasi lengkap dan terorganisir
- ✅ Fully backward compatible
- ✅ Output files di project root (bukan di skill folder)
- ✅ Generic naming (tidak ada branding spesifik)
- ✅ Baseline template untuk reference

## 🔄 Workflow

```
1. Setup .env file dengan AWS credentials
   ↓
2. Run: python scripts/generate-from-env.py
   ↓
3. Scan AWS Resources (automatic)
   ↓
4. Generate Technical Document (Professional Format)
   ↓
5. Review and Finalize
   ↓
6. Deliver to Client
```

## 📖 Document Structure (Professional Format)

The generated professional format document includes:

1. **Cover Page** - Professional branding
2. **Table of Contents** - Document navigation
3. **Confidentiality Agreement** - Legal protection
4. **Document Control** - Version tracking & signatures
5. **Section 1: AWS Solution Overview** - Architecture diagram & services
6. **Section 2: AWS Resource List** - Comprehensive tables
7. **Section 3: Security** - Best practices & configurations
8. **Section 4: Cost Optimization** - Recommendations & strategies
9. **Section 5: Tutorial** - Step-by-step implementation guides

## 🐛 Troubleshooting

### Error: boto3 not found
```bash
pip install boto3
```

### Error: .env not found
```bash
cp .env.example .env
# Then edit .env with your credentials
```

### Error: Invalid credentials
Check your AWS credentials in `.env` file

### Files not in root directory
Check that you're running from the skill folder and that `.kiro` folder exists in parent directories

## 📞 Support

For issues or questions:
- Check the troubleshooting section
- Review documentation files
- Contact Cloud Engineering Team

---

**Version**: 2.0.0  
**Last Updated**: February 21, 2026  
**License**: MIT
