# Cara Menggunakan AWS Technical Document Generator

Panduan praktis untuk membuat dokumentasi teknis AWS secara otomatis.

## Apa yang Dilakukan Tool Ini?

Tool ini membantu Anda membuat dokumentasi teknis AWS dengan cara:
1. Scan semua resources di AWS account Anda
2. Kumpulkan informasi detail dari setiap resource
3. Generate document markdown yang terstruktur dan siap pakai

---

## Setup Awal (Hanya Sekali)

### Langkah 1: Install Dependencies

```bash
cd .kiro/skills/aws-technical-doc-generator
pip install -r requirements.txt
```

### Langkah 2: Buat IAM User untuk Scanning

**PENTING**: Gunakan IAM user dengan **READ-ONLY permission** saja!

1. Login ke AWS Console
2. Buka **IAM** → **Users** → **Add User**
3. User name: `aws-doc-generator`
4. Access type: **Programmatic access**
5. Attach policy: Gunakan template di `references/iam-policy-template.json`
6. Simpan **Access Key ID** dan **Secret Access Key**

### Langkah 3: Setup File .env

```bash
# Copy file template
cp .env.example .env

# Edit file .env dengan text editor
notepad .env   # Windows
nano .env      # Linux/Mac
```

Isi file `.env` dengan informasi Anda:

```bash
# AWS Credentials
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_DEFAULT_REGION=ap-southeast-1

# Project Information
PROJECT_NAME=SAP HANA Migration
CUSTOMER_NAME=PT Telkom Indonesia

# Document Version
DOCUMENT_VERSION=1.0
```

**PENTING**: 
- Jangan commit file `.env` ke Git!
- File `.env` sudah ada di `.gitignore`

---

## Cara Menggunakan

### Metode 1: Menggunakan File .env (RECOMMENDED)

Ini cara paling mudah karena semua konfigurasi sudah ada di file `.env`:

**DEFAULT: Format KCI (Professional)**

```bash
# Pastikan sudah di folder skill
cd .kiro/skills/aws-technical-doc-generator

# Load environment variables dari .env
# Windows (CMD):
for /f "delims=" %i in (.env) do set %i

# Windows (PowerShell):
Get-Content .env | ForEach-Object { if($_ -match '^([^=]+)=(.*)$') { [Environment]::SetEnvironmentVariable($matches[1], $matches[2]) } }

# Linux/Mac:
export $(cat .env | xargs)

# Jalankan generator (menggunakan KCI format secara default)
python scripts/generate-from-env.py
```

Output: `Technical-Document-[Customer]-[Project]-v[Version]-KCI.md`

**Alternatif: Format Standard (Simple)**

Jika Anda ingin menggunakan format standard yang lebih sederhana:

```bash
python scripts/generate-from-env-standard.py
```

Output: `Technical-Document-[Customer]-[Project]-v[Version].md`

### Metode 2: Manual (Tanpa .env)

Jika tidak ingin menggunakan file `.env`:

```bash
# Step 1: Scan AWS resources
python scripts/scan-aws-resources.py "YOUR_ACCESS_KEY" "YOUR_SECRET_KEY" "ap-southeast-1"

# Output: aws-resources-20240221-143022.json

# Step 2: Generate document
python scripts/generate-document.py "aws-resources-20240221-143022.json" "PT Telkom Indonesia" "SAP HANA Migration" "1.0"

# Output: Technical-Document-PTTelkomIndonesia-SAPHANAMigration-v1.0.md
```

### Metode 3: Interactive Mode (Coming Soon)

```bash
kiro use aws-technical-doc-generator
```

---

## Output yang Dihasilkan

**PENTING**: Semua file output akan disimpan di **root directory project** (bukan di dalam folder skill) agar folder skill tetap bersih.

**DEFAULT: Format KCI (Professional)**

### 1. File Scan Results (JSON)
```
<project-root>/aws-resources-20240221-143022.json
```
File ini berisi semua data mentah dari AWS resources dan disimpan di root directory project Anda.

### 2. Technical Document (Markdown) - KCI Format
```
<project-root>/Technical-Document-PTTelkomIndonesia-SAPHANAMigration-v1.0-KCI.md
```
File ini adalah dokumentasi teknis profesional dengan format KCI yang siap pakai dan disimpan di root directory project Anda.

**Format KCI mencakup:**
- Cover page profesional dengan branding
- Confidentiality agreement
- Document control dengan version tracking
- 5 section lengkap (Overview, Resources, Security, Cost Optimization, Tutorial)
- Tabel komprehensif untuk semua AWS resources
- Tutorial step-by-step

**Alternatif: Format Standard (Simple)**

Jika menggunakan `generate-from-env-standard.py`:
```
<project-root>/Technical-Document-PTTelkomIndonesia-SAPHANAMigration-v1.0.md
```
Format standard lebih sederhana, cocok untuk dokumentasi internal.

### Contoh Output Saat Scanning

```
🚀 Starting AWS Resource Scan
============================================================

✅ Credentials validated
   Account ID: 123456789012
   Region: ap-southeast-1

🔍 Scanning VPC and networking...
🔍 Scanning EC2 instances...
🔍 Scanning EBS volumes...
🔍 Scanning Load Balancers...
🔍 Scanning RDS databases...
🔍 Scanning S3 buckets...
🔍 Scanning Security Groups...
🔍 Scanning IAM resources...
🔍 Scanning CloudWatch alarms...
🔍 Scanning Auto Scaling groups...

============================================================
✅ Scan Complete!
============================================================

Resources Found:
  - VPCs: 1
  - EC2 Instances: 12
  - EBS Volumes: 24 (2,400 GB)
  - Load Balancers: 2
  - RDS Instances: 3
  - S3 Buckets: 8
  - Security Groups: 15
  - CloudWatch Alarms: 8
  - Auto Scaling Groups: 2

📄 Results saved to: aws-resources-20240221-143022.json
```

### Contoh Output Saat Generate Document

```
============================================================
📝 Generating Technical Document
============================================================

✅ Document generation complete!

📄 Document saved to: Technical-Document-PTTelkomIndonesia-SAPHANAMigration-v1.0.md
```

---

## Isi Document yang Dihasilkan

Document akan berisi 10 section utama:

1. **Executive Summary** - Overview project dan key metrics
2. **Network Architecture** - VPC, subnets, routing
3. **Compute Resources** - EC2 instances dan detail
4. **Storage Resources** - EBS volumes
5. **Load Balancing** - ALB/NLB dan target groups
6. **Database Resources** - RDS instances
7. **S3 Storage** - S3 buckets dengan encryption info
8. **Security Configuration** - Security groups dan rules
9. **Monitoring and Logging** - CloudWatch alarms
10. **Conclusion** - Summary dan contact info

---

## Troubleshooting

### ❌ Error: boto3 tidak ditemukan
```bash
pip install boto3
```

### ❌ Error: Invalid credentials
```bash
# Test credentials
aws sts get-caller-identity

# Periksa:
# 1. Access Key ID benar?
# 2. Secret Access Key benar?
# 3. IAM user masih aktif?
```

### ❌ Error: Permission denied
```bash
# Gunakan IAM policy template di:
# references/iam-policy-template.json
```

### ❌ Error: File .env tidak ditemukan
```bash
# Copy dari template
cp .env.example .env

# Edit dengan credentials Anda
notepad .env
```

### ❌ Error: Resource tidak muncul di document
Kemungkinan penyebab:
- IAM permissions tidak lengkap
- Resource ada di region berbeda
- Resource tidak memiliki tags

---

## Tips Keamanan

### ✅ DO (Lakukan)
- Gunakan IAM user dengan **READ-ONLY** permission
- Simpan credentials di file `.env` (sudah di `.gitignore`)
- Rotate access keys setiap 90 hari
- Review document sebelum share

### ❌ DON'T (Jangan)
- Commit file `.env` ke Git
- Share credentials via email/chat
- Gunakan root account credentials
- Hardcode credentials di script

---

## Workflow untuk Tim

### Untuk Project Baru

1. **Setup** (sekali saja)
   ```bash
   cd .kiro/skills/aws-technical-doc-generator
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env dengan credentials
   ```

2. **Generate Document**
   ```bash
   # Load .env
   export $(cat .env | xargs)
   
   # Scan dan generate
   python scripts/scan-aws-resources.py $AWS_ACCESS_KEY_ID $AWS_SECRET_ACCESS_KEY $AWS_DEFAULT_REGION
   python scripts/generate-document.py aws-resources-*.json "$CUSTOMER_NAME" "$PROJECT_NAME" $DOCUMENT_VERSION
   ```

3. **Review dan Share**
   - Review document yang dihasilkan
   - Commit ke Git (document saja, bukan .env!)
   - Share dengan stakeholders

### Untuk Update Document

1. **Update versi di .env**
   ```bash
   # Edit .env
   DOCUMENT_VERSION=1.1  # atau 2.0 untuk major changes
   ```

2. **Re-scan dan generate**
   ```bash
   # Jalankan ulang scripts
   python scripts/scan-aws-resources.py ...
   python scripts/generate-document.py ...
   ```

3. **Compare dengan versi sebelumnya**
   ```bash
   # Gunakan Git diff
   git diff Technical-Document-*.md
   ```

---

## Quick Reference

### File Penting

| File | Fungsi |
|------|--------|
| `.env` | Konfigurasi credentials dan project info |
| `.env.example` | Template untuk `.env` |
| `scripts/scan-aws-resources.py` | Script untuk scan AWS |
| `scripts/generate-document.py` | Script untuk generate document |
| `references/iam-policy-template.json` | IAM policy template |

### Command Cheat Sheet

```bash
# Setup awal
pip install -r requirements.txt
cp .env.example .env

# Load environment variables (Linux/Mac)
export $(cat .env | xargs)

# Load environment variables (Windows PowerShell)
Get-Content .env | ForEach-Object { if($_ -match '^([^=]+)=(.*)$') { [Environment]::SetEnvironmentVariable($matches[1], $matches[2]) } }

# Scan AWS
python scripts/scan-aws-resources.py $AWS_ACCESS_KEY_ID $AWS_SECRET_ACCESS_KEY $AWS_DEFAULT_REGION

# Generate document
python scripts/generate-document.py aws-resources-*.json "$CUSTOMER_NAME" "$PROJECT_NAME" $DOCUMENT_VERSION
```

---

## Bantuan Lebih Lanjut

### Dokumentasi Lengkap
- **QUICKSTART.md** - Panduan cepat 5 menit untuk mulai
- **TEAM-GUIDE.md** - Panduan khusus untuk tim (workflow, tips, troubleshooting)
- **README-ID.md** - README dalam bahasa Indonesia
- **SKILL.md** - Dokumentasi teknis lengkap
- **Setup Guide**: `references/setup-guide.md` - Panduan setup IAM
- **Project Structure**: `PROJECT-STRUCTURE.md` - Struktur file dan folder

### File Penting
- `.env` - File konfigurasi Anda (JANGAN COMMIT!)
- `.env.example` - Template untuk `.env`
- `scripts/generate-from-env.py` - Script utama (RECOMMENDED)
- `scripts/run-with-env.bat` - Script untuk Windows
- `scripts/run-with-env.sh` - Script untuk Linux/Mac

### Kontak
Jika ada pertanyaan atau masalah, hubungi Cloud Engineering team.

---

**Selamat menggunakan AWS Technical Document Generator!** 🚀
