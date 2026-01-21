import argparse
import sys
from scanner_core import scan_github_repo, scan_s3_bucket
from folder_scanner import scan_local_folder

def print_summary(summary):
    print(f"Files scanned: {summary.get('files_scanned', 0)}")
    if summary.get('info'):
        print(f"Info: {summary['info']}")
    if summary.get('errors'):
        print("Errors:")
        for err in summary['errors']:
            print(f"  - {err}")
    if summary.get('findings'):
        print("Findings:")
        for fname, fdata in summary['findings'].items():
            print(f"  {fname}:")
            for k, v in fdata.items():
                print(f"    {k}: {v}")
    else:
        print("No sensitive data found.")

def main():
    parser = argparse.ArgumentParser(description="Privacy Risk Analyzer: Scan public data for sensitive information leaks.")
    subparsers = parser.add_subparsers(dest="command")

    github_parser = subparsers.add_parser("github", help="Scan a GitHub repository")
    github_parser.add_argument("repo_url", help="GitHub repository URL")

    s3_parser = subparsers.add_parser("s3", help="Scan an AWS S3 bucket")
    s3_parser.add_argument("bucket_name", help="S3 bucket name")

    local_parser = subparsers.add_parser("local", help="Scan a local folder recursively")
    local_parser.add_argument("folder_path", help="Path to local folder")

    args = parser.parse_args()

    if args.command == "github":
        summary = scan_github_repo(args.repo_url)
        print_summary(summary)
    elif args.command == "s3":
        summary = scan_s3_bucket(args.bucket_name)
        print_summary(summary)
    elif args.command == "local":
        summary = scan_local_folder(args.folder_path)
        print_summary(summary)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
