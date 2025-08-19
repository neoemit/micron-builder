#!/usr/bin/env python3
import re
import sys
from pathlib import Path
import subprocess

PYPROJECT = Path("pyproject.toml")

def get_current_version():
    text = PYPROJECT.read_text()
    match = re.search(r'version\s*=\s*"([^"]+)"', text)
    if not match:
        print("❌ Could not find version in pyproject.toml")
        sys.exit(1)
    return match.group(1)

def set_version(new_version):
    text = PYPROJECT.read_text()
    new_text = re.sub(
        r'(version\s*=\s*")[^"]+(")',
        fr'\g<1>{new_version}\g<2>',
        text,
    )
    PYPROJECT.write_text(new_text)

def main():
    if len(sys.argv) != 2:
        print("Usage: bump_version.py <new_version>")
        sys.exit(1)

    new_version = sys.argv[1]
    old_version = get_current_version()
    print(f"🔄 Bumping version: {old_version} → {new_version}")

    set_version(new_version)

    # Commit and tag
    subprocess.run(["git", "add", "pyproject.toml"], check=True)
    subprocess.run(["git", "commit", "-m", f"Release v{new_version}"], check=True)
    subprocess.run(["git", "tag", f"v{new_version}"], check=True)

    print(f"✅ Updated to version {new_version}. Don't forget to push with:")
    print("   git push origin main --tags")

if __name__ == "__main__":
    main()
