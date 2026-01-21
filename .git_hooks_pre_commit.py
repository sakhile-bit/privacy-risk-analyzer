# Example pre-commit hook for local secret scanning
# Save as .git/hooks/pre-commit and make executable
import sys
import subprocess

print('Running local secret scan...')
result = subprocess.run([sys.executable, 'main.py', 'local', '.'])
if result.returncode != 0:
    print('Secret scan failed! Commit aborted.')
    sys.exit(1)
