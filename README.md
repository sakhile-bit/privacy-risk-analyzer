# Privacy Risk Analyzer for Public Data

## Overview

This tool scans public datasets (such as GitHub repositories and S3 buckets) for sensitive information leaks, including API keys, credentials, and PII. It provides both a CLI and a web dashboard, and is designed for extensibility and community contributions.

## Features

- Scan all GitHub repositories for a user/org (with token support)
- Scan AWS S3 buckets (public or private, with AWS credentials)
- Detect API keys, credentials, PII, secrets, tokens, and more using advanced regex patterns
- CLI interface for quick scans with scan summary and findings
- Web dashboard for results visualization, scan summary, and error reporting
- Plugin system: drop in new Python detection rules in the `plugins/` folder
- Local folder scan (recursively scan all files)
- Slack and Email alerts for findings
- GitHub Action workflow for CI/CD integration
- Pre-commit hook for local secret scanning
- Dashboard authentication and persistent scan history (coming soon)
- Export results as JSON/CSV from the dashboard (coming soon)

## Getting Started

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt` (add `boto3` for private S3 support)
3. Run CLI:
   - `python main.py github https://github.com/owner/repo`
   - `python main.py s3 public-bucket-name`
   - `python main.py local /path/to/folder`
4. Launch web dashboard: `python webapp.py` and open http://127.0.0.1:5000
5. To add custom detection, drop a Python file with a `detect(text)` function in the `plugins/` folder.
6. To enable alerts, configure and use `email_alert.py` or `slack_alert.py`.
7. For CI/CD, see `.github/workflows/scan.yml`. For pre-commit, see `.git_hooks_pre_commit.py`.

## Example Output

CLI output:

```
Files scanned: 1
Findings:
	README.md:
		Email: ['example@email.com']
		AWS Access Key: ['AKIA...']
	Plugins:
		todo_plugin: {'TODOs': ['TODO: fix this']}
No sensitive data found.
```

Web dashboard:

- Shows scan summary, errors, and findings in a user-friendly format.

## Contributing

- Fork the repo and submit pull requests
- Add new plugins for data sources or detection rules (see `plugins/`)
- Improve detection accuracy and performance
- Add integrations (alerts, export, dashboard features)

## License

MIT
"# privacy-risk-analyzer" 
