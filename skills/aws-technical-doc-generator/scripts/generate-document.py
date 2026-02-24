#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Technical Document Generator - Default (Professional Format)
This is an alias to generate-document-professional.py
Generates formatted technical documentation from AWS resource scan data using professional template.
"""

import sys
import subprocess

def main():
    """Forward to Professional format generator."""
    # Forward all arguments to the Professional format generator
    cmd = ['python', 'scripts/generate-document-professional.py'] + sys.argv[1:]
    result = subprocess.run(cmd)
    sys.exit(result.returncode)

if __name__ == '__main__':
    main()
