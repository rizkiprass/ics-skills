# Quick Start Guide

Panduan cepat untuk mulai menggunakan AWS Technical Document Generator dalam 5 menit.

## Langkah 1: Install Dependencies (1 menit)

```bash
cd .kiro/skills/aws-technical-doc-generator
pip install -r requirements.txt
```

## Langkah 2: Setup File .env (2 menit)

```bash
# Copy template
cp .env.example .env

# Edit dengan text editor
notepad .env   # Windows
nano .env      # Linux/Mac
```

Isi dengan informasi Anda:

```bash
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_DEFAULT_REGION=ap-southeast-1

PROJECT_NAME=SAP HANA Migration
CUSTOMER_NAME=PT Telkom Indonesia
DOCUMENT_VERSION=1.0
```

## Langkah 3: Generate Document (2 menit)

### Opsi A: Menggunakan Python Script (Semua Platform) - RECOMMENDED

**DEFAULT: Format KCI (Professional)**
```bash
python scripts/generate-from-env.py
```

**Alternatif: Format Standard (Simple)**
```bash
python scripts/generate-from-env-standard.py
```

### Opsi B: Menggunakan Shell Script

#### Windows
```bash
scripts\run-with-env.bat
```

#### Linux/Mac
```bash
chmod +x scripts/run-with-env.sh
./scripts/run-with-env.sh
```

## Selesai! 🎉

Document Anda akan tersimpan di **root directory project** dengan nama:

**Format KCI (Default - Professional):**
```
<project-root>/Technical-Document-[CustomerName]-[ProjectName]-v[Version]-KCI.md
```

**Format Standard (Alternatif - Simple):**
```
<project-root>/Technical-Document-[CustomerName]-[ProjectName]-v[Version].md
```

File scan results juga akan tersimpan di root directory:
```
<project-root>/aws-resources-YYYYMMDD-HHMMSS.json
```

**Format KCI mencakup:**
- ✅ Cover page profesional
- ✅ Confidentiality agreement
- ✅ Document control & signatures
- ✅ Comprehensive resource tables
- ✅ Security best practices
- ✅ Cost optimization recommendations
- ✅ Step-by-step tutorials

---

## Troubleshooting Cepat

### Error: boto3 tidak ditemukan
```bash
pip install boto3
```

### Error: File .env tidak ditemukan
```bash
cp .env.example .env
# Edit .env dengan credentials Anda
```

### Error: Invalid credentials
Periksa AWS credentials di file `.env` sudah benar.

---

## Next Steps

- Baca **HOW-TO-USE.md** untuk panduan lengkap
- Review document yang dihasilkan
- Share dengan team Anda

**Butuh bantuan?** Hubungi Cloud Engineering team.
