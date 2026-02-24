#!/usr/bin/env python3
"""
AWS Technical Document Generator - Main Script
Reads configuration from .env file and generates technical documentation.
Default format: KCI Template (Professional)
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

def get_project_root():
    """Get the project root directory (where .kiro folder exists)."""
    current = Path(__file__).resolve()
    # Navigate up from scripts/ to skill folder to .kiro/ to project root
    for parent in current.parents:
        if (parent / '.kiro').exists():
            return parent
    # Fallback to current directory
    return Path.cwd()

def load_env_file(env_path='.env'):
    """Load environment variables from .env file."""
    if not os.path.exists(env_path):
        print(f"❌ Error: File {env_path} tidak ditemukan!")
        print()
        print("Silakan copy dari template:")
        print("  cp .env.example .env")
        print()
        print("Kemudian edit file .env dengan credentials Anda.")
        sys.exit(1)
    
    env_vars = {}
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            
            # Parse key=value
            if '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    
    return env_vars

def validate_config(config):
    """Validate required configuration variables."""
    required = [
        'AWS_ACCESS_KEY_ID',
        'AWS_SECRET_ACCESS_KEY',
        'AWS_DEFAULT_REGION',
        'CUSTOMER_NAME',
        'PROJECT_NAME',
        'DOCUMENT_VERSION'
    ]
    
    missing = []
    for key in required:
        if key not in config or not config[key]:
            missing.append(key)
    
    if missing:
        print("❌ Error: Konfigurasi tidak lengkap di .env")
        print()
        print("Variable yang hilang:")
        for key in missing:
            print(f"  - {key}")
        print()
        sys.exit(1)
    
    return True

def main():
    """Main entry point."""
    print()
    print("=" * 60)
    print("AWS Technical Document Generator")
    print("=" * 60)
    print()
    
    # Get project root
    project_root = get_project_root()
    
    # Load .env file
    print("✓ Loading configuration from .env...")
    config = load_env_file('.env')
    
    # Validate configuration
    validate_config(config)
    
    print("✓ Configuration loaded successfully")
    print()
    print(f"  Customer: {config['CUSTOMER_NAME']}")
    print(f"  Project: {config['PROJECT_NAME']}")
    print(f"  Version: {config['DOCUMENT_VERSION']}")
    print(f"  Region: {config['AWS_DEFAULT_REGION']}")
    print(f"  Output Directory: {project_root}")
    print(f"  Format: Professional Template")
    print()
    
    # Step 1: Scan AWS resources
    print("=" * 60)
    print("Step 1: Scanning AWS resources...")
    print("=" * 60)
    print()
    
    scan_cmd = [
        'python',
        'scripts/scan-aws-resources.py',
        config['AWS_ACCESS_KEY_ID'],
        config['AWS_SECRET_ACCESS_KEY'],
        config['AWS_DEFAULT_REGION']
    ]
    
    result = subprocess.run(scan_cmd, capture_output=True, text=True)
    print(result.stdout)
    
    if result.returncode != 0:
        print("❌ Error: Scan failed")
        print(result.stderr)
        sys.exit(1)
    
    # Find the latest scan file in project root
    scan_files = sorted(project_root.glob('aws-resources-*.json'))
    if not scan_files:
        print("❌ Error: Scan file tidak ditemukan")
        sys.exit(1)
    
    scan_file = str(scan_files[-1])
    print()
    print(f"✓ Scan completed: {scan_file}")
    print()
    
    # Step 2: Generate document using Professional format (default)
    print("=" * 60)
    print("Step 2: Generating technical document...")
    print("=" * 60)
    print()
    
    gen_cmd = [
        'python',
        'scripts/generate-document-professional.py',
        scan_file,
        config['CUSTOMER_NAME'],
        config['PROJECT_NAME'],
        config['DOCUMENT_VERSION']
    ]
    
    result = subprocess.run(gen_cmd, capture_output=True, text=True)
    print(result.stdout)
    
    if result.returncode != 0:
        print("❌ Error: Document generation failed")
        print(result.stderr)
        sys.exit(1)
    
    # Step 3: Convert to DOCX
    print("=" * 60)
    print("Step 3: Converting to DOCX format...")
    print("=" * 60)
    print()
    
    # Find the generated markdown file
    customer_clean = config['CUSTOMER_NAME'].replace(' ', '')
    project_clean = config['PROJECT_NAME'].replace(' ', '')
    md_filename = f"Technical-Document-{customer_clean}-{project_clean}-v{config['DOCUMENT_VERSION']}.md"
    md_file = project_root / md_filename
    
    if not md_file.exists():
        print(f"⚠️  Warning: Markdown file not found: {md_file}")
        print("Skipping DOCX conversion")
    else:
        # Check if Node.js is available
        try:
            node_check = subprocess.run(['node', '--version'], capture_output=True, text=True)
            if node_check.returncode != 0:
                print("⚠️  Warning: Node.js not found. Skipping DOCX conversion.")
                print("To enable DOCX conversion, install Node.js and run: npm install")
            else:
                # Get the skill directory
                skill_dir = Path(__file__).resolve().parent.parent
                
                # Check if local node_modules exists
                node_modules = skill_dir / 'node_modules'
                if not node_modules.exists():
                    print("⚠️  Warning: Node.js dependencies not installed.")
                    print("To enable DOCX conversion, run: npm install")
                else:
                    # Run conversion with absolute path
                    convert_script = skill_dir / 'scripts' / 'convert-md-to-docx.js'
                    convert_cmd = ['node', str(convert_script), str(md_file)]
                    result = subprocess.run(convert_cmd, capture_output=True, text=True, cwd=str(skill_dir))
                    print(result.stdout)
                    
                    if result.returncode != 0:
                        print("⚠️  Warning: DOCX conversion failed")
                        print(result.stderr)
                    else:
                        docx_filename = md_filename.replace('.md', '.docx')
                        print(f"✓ DOCX document created: {docx_filename}")
        except FileNotFoundError:
            print("⚠️  Warning: Node.js not found. Skipping DOCX conversion.")
            print("To enable DOCX conversion, install Node.js and run: npm install")
    
    print()
    print("=" * 60)
    print("✓ Process completed successfully!")
    print("=" * 60)
    print()
    print("Generated files:")
    print(f"  - Markdown: {md_filename}")
    if (project_root / md_filename.replace('.md', '.docx')).exists():
        print(f"  - Word: {md_filename.replace('.md', '.docx')}")
    print()
    print("Note: Using Professional Template format (default)")
    print("For standard format, use: python scripts/generate-from-env-standard.py")
    print()

if __name__ == '__main__':
    main()
