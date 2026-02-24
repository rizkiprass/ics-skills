# Bug Fix Notes - AWS Technical Document Generator

## Issue
Dokumen teknis yang di-generate menampilkan "N/A" untuk semua resource AWS, padahal data scanning sudah berhasil mengumpulkan informasi lengkap.

## Root Cause
Script `generate-document-professional.py` menggunakan field names yang salah saat membaca data dari JSON hasil scanning AWS. Script mencari field dengan lowercase/snake_case (misalnya `vpc.get('name')`, `vpc.get('vpc_id')`), sedangkan data AWS menggunakan PascalCase (misalnya `VpcId`, `CidrBlock`) dan Tags dalam format list of dictionaries.

## Solution
1. **Menambahkan helper method `get_tag_value()`** untuk mengekstrak nilai dari AWS Tags
2. **Menambahkan helper method `get_instance_specs()`** untuk mendapatkan CPU dan Memory dari instance type
3. **Memperbaiki semua field mappings** di method-method berikut:
   - `generate_vpc_section()`: Menggunakan `VpcId`, `CidrBlock`, dan `Tags`
   - `generate_subnet_section()`: Menggunakan `SubnetId`, `AvailabilityZone`, `CidrBlock`, dan `Tags`
   - `generate_ec2_section()`: Menggunakan `InstanceId`, `InstanceType`, `PlatformDetails`, `PublicIpAddress`, `PrivateIpAddress`, dan `Tags`
   - `generate_security_groups_section()`: Menggunakan `GroupName`, `GroupId`, `Description`, `IpPermissions`, `IpPermissionsEgress`
   - `generate_iam_section()`: Menggunakan `UserName`, `Groups`, `MFAEnabled`

4. **Membuat script perbaikan sementara** (`fix-document.py`) untuk memperbaiki dokumen yang sudah di-generate

## Files Modified
- `.kiro/skills/aws-technical-doc-generator/scripts/generate-document-professional.py` - Script generator utama
- `.kiro/skills/aws-technical-doc-generator/scripts/fix-document.py` - Script perbaikan (NEW)

## Testing
Dokumen `Technical-Document-PTMaju-webreactmigrationtoaws-v1.0.md` sudah berhasil diperbaiki dan menampilkan:
- ✅ 1 VPC (project-vpc)
- ✅ 4 Subnets (2 public, 2 private)
- ✅ 2 EC2 instances (test1, test2) dengan spesifikasi lengkap
- ✅ 3 Security Groups dengan inbound/outbound rules
- ✅ 3 S3 Buckets
- ✅ 4 IAM Users

## Next Steps
Untuk generate dokumen baru di masa depan, gunakan script yang sudah diperbaiki:
```bash
python scripts/generate-from-env.py
```

Script akan otomatis menggunakan field mappings yang benar.

## Date
February 21, 2026
