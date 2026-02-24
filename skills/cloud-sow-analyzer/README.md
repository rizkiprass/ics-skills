# Cloud SOW Analyzer

Skill untuk menganalisis dokumen Scope of Work (SOW) proyek cloud migration dan menghasilkan risk assessment komprehensif.

## Deskripsi

Cloud SOW Analyzer membantu Cloud Architect menganalisis dokumen SOW untuk proyek cloud migration ke AWS atau Huawei Cloud. Skill ini akan:

- Membaca dan mengekstrak informasi dari file DOCX SOW
- Menanyakan informasi yang kurang sebelum melakukan analisis
- Mengidentifikasi risiko untuk migration dan implementation
- Menemukan potensi masalah di awal proyek
- Menghasilkan laporan analisis lengkap dalam format markdown

## Kapan Menggunakan Skill Ini

Gunakan skill ini ketika Anda:
- Menerima dokumen SOW baru untuk proyek cloud migration
- Perlu melakukan risk assessment sebelum memulai migration
- Ingin mengidentifikasi potensi masalah sejak awal
- Membutuhkan analisis terstruktur dari dokumen SOW
- Perlu validasi kelengkapan informasi dalam SOW

## Instalasi

### Untuk GitHub Copilot CLI

```bash
# Clone repository
git clone https://github.com/yourusername/cli-ai-skills.git

# Symlink ke direktori skills Copilot
ln -sf "$(pwd)/cli-ai-skills/skills/cloud-sow-analyzer" \
       "$HOME/.copilot/skills/cloud-sow-analyzer"
```

### Untuk Claude Code

```bash
# Symlink ke direktori skills Claude
ln -sf "$(pwd)/cli-ai-skills/skills/cloud-sow-analyzer" \
       "$HOME/.claude/skills/cloud-sow-analyzer"
```

## Cara Menggunakan

### Basic Usage

```bash
# Analyze SOW document
analyze-sow migration-project-sow.docx
```

Skill akan:
1. Membaca file DOCX
2. Menanyakan informasi yang kurang (cloud provider, timeline, dll)
3. Melakukan analisis risiko
4. Menghasilkan report dalam format markdown

### Output

Skill akan menghasilkan file markdown dengan struktur:
- Executive Summary
- SOW Analysis (completeness check)
- Risk Assessment (dengan scoring matrix)
- Issues & Findings (prioritized)
- Architecture Analysis
- Resource Analysis
- Implementation Plan Analysis
- Recommendations (actionable items)
- Discovery Phase Checklist

## Contoh Output

```markdown
# Cloud Migration SOW Analysis Report

**Project:** E-Commerce Platform Migration
**Cloud Provider:** AWS
**Analysis Date:** 2026-02-21

## Risk Summary
🔴 Critical: 2 risks
🟠 High: 5 risks
🟡 Medium: 6 risks
🟢 Low: 2 risks

## Top Recommendations
1. Define rollback strategy (Critical)
2. Complete dependency mapping (High)
3. Validate resource sizing (High)
```

## Cloud Provider Support

- **AWS**: Full support dengan AWS-specific best practices
- **Huawei Cloud**: Full support dengan Huawei Cloud-specific considerations

## Fitur Utama

1. **Interactive Clarification** - Menanyakan info yang kurang sebelum analisis
2. **Risk Scoring Matrix** - Probability × Impact scoring
3. **Multi-dimensional Analysis** - Technical, Operational, Security, Financial, Vendor risks
4. **Actionable Recommendations** - Prioritized dengan timeline
5. **Discovery Checklist** - Ready-to-use checklist untuk project kickoff

## Requirements

- File SOW dalam format DOCX
- Pandoc atau python-docx untuk ekstraksi konten (optional)
- Informasi tambahan tentang project context

## Tips

- Pastikan SOW document lengkap sebelum analisis
- Siapkan informasi tambahan yang mungkin ditanyakan (timeline, budget, compliance requirements)
- Review report dengan stakeholders
- Update analysis saat project evolves

## Troubleshooting

**File DOCX tidak bisa dibaca?**
- Coba convert ke PDF terlebih dahulu
- Atau copy-paste content secara manual

**Analysis tidak lengkap?**
- Provide missing information saat ditanya
- Atau update SOW document

## Support

Untuk pertanyaan atau issues, silakan contact skill maintainer atau check dokumentasi lengkap di SKILL.md.

## License

Community contribution - provided as-is for cloud migration analysis purposes.

