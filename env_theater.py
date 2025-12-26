#!/usr/bin/env python3
"""ENV Var Theater - Because your environment variables are putting on a show!"""

import os
import sys
import glob
from pathlib import Path

def find_env_files():
    """Find all the .env files hiding in your codebase like shy actors."""
    patterns = ['.env*', '*.env', 'docker-compose*.yml', 'Dockerfile*', '*.sh']
    env_files = []
    
    for pattern in patterns:
        for file in glob.glob(pattern, recursive=True):
            if os.path.isfile(file):
                env_files.append(file)
    
    # Add current environment for the dramatic finale
    env_files.append('(runtime environment)')
    return sorted(set(env_files))

def scan_file(filepath, target_var=None):
    """Read a file and find all the ENV drama."""
    results = []
    
    if filepath == '(runtime environment)':
        if target_var:
            value = os.environ.get(target_var, '(not set)')
            results.append(f"  {target_var}: {value}")
        else:
            for key in sorted(os.environ.keys()):
                results.append(f"  {key}: {os.environ[key]}")
        return results
    
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
    except (IOError, UnicodeDecodeError):
        return ["  (could not read file)"]
    
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if target_var:
            if target_var in line and ('=' in line or 'export ' in line or 'ENV ' in line):
                results.append(f"  Line {i}: {line}")
        else:
            # Look for common ENV patterns
            if any(pattern in line for pattern in ['=', 'export ', 'ENV ', 'env:', 'environment:']):
                results.append(f"  Line {i}: {line}")
    
    return results if results else ["  (no env vars found)"]

def main():
    """The main performance begins!"""
    if len(sys.argv) > 2:
        print("Usage: python env_theater.py [VARIABLE_NAME]")
        print("Example: python env_theater.py DATABASE_URL")
        sys.exit(1)
    
    target_var = sys.argv[1] if len(sys.argv) == 2 else None
    
    print("\n🎭 ENVIRONMENT VARIABLE THEATER 🎭")
    print("Starring all your scattered configuration!\n")
    
    env_files = find_env_files()
    
    for filepath in env_files:
        print(f"📁 {filepath}")
        print("-" * 40)
        
        for result in scan_file(filepath, target_var):
            print(result)
        
        print()
    
    print("🎬 Curtain call! Check which variable is actually on stage at runtime!")

if __name__ == "__main__":
    main()