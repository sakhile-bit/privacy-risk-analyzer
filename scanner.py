import re
import requests

def scan_github_repo(repo_url):
    # For demo, just fetch README.md if exists
    api_url = repo_url.replace('https://github.com/', 'https://raw.githubusercontent.com/') + '/main/README.md'
    summary = {"files_scanned": 0, "findings": {}, "errors": []}
    try:
        resp = requests.get(api_url)
        summary["files_scanned"] = 1
        if resp.status_code == 200:
            findings = scan_text(resp.text)
            if findings:
                summary["findings"]["README.md"] = findings
        else:
            summary["errors"].append("Could not fetch README.md for scanning.")
    except Exception as e:
        summary["errors"].append(str(e))
    return summary

def scan_s3_bucket(bucket_name):
    # Try to list and scan files in a public or private S3 bucket (list up to 5 files)
    summary = {"files_scanned": 0, "findings": {}, "errors": []}
    try:
        try:
            import boto3
            s3 = boto3.client('s3')
            resp = s3.list_objects_v2(Bucket=bucket_name, MaxKeys=5)
            if 'Contents' not in resp:
                summary["errors"].append(f"No files found or access denied for bucket {bucket_name}.")
                return summary
            for obj in resp['Contents']:
                key = obj['Key']
                file_obj = s3.get_object(Bucket=bucket_name, Key=key)
                content = file_obj['Body'].read().decode('utf-8', errors='ignore')
                summary["files_scanned"] += 1
                file_findings = scan_text(content)
                if file_findings:
                    summary["findings"][key] = file_findings
        except ImportError:
            # Fallback to requests for public buckets
            import xml.etree.ElementTree as ET
            url = f"https://{bucket_name}.s3.amazonaws.com/"
            resp = requests.get(url)
            if resp.status_code != 200:
                summary["errors"].append(f"Could not access bucket {bucket_name}. Is it public?")
                return summary
            tree = ET.fromstring(resp.text)
            keys = [elem.text for elem in tree.findall('.//{http://s3.amazonaws.com/doc/2006-03-01/}Key')]
            for key in keys[:5]:
                file_url = f"https://{bucket_name}.s3.amazonaws.com/{key}"
                file_resp = requests.get(file_url)
                summary["files_scanned"] += 1
                if file_resp.status_code == 200:
                    file_findings = scan_text(file_resp.text)
                    if file_findings:
                        summary["findings"][key] = file_findings
                else:
                    summary["errors"].append(f"Could not fetch {key}")
        if not summary["findings"] and not summary["errors"]:
            summary["info"] = "No sensitive data found in first 5 files."
        return summary
    except Exception as e:
        summary["errors"].append(str(e))
        return summary
import re
import requests

def scan_github_repo(repo_url):
    # For demo, just fetch README.md if exists
    api_url = repo_url.replace('https://github.com/', 'https://raw.githubusercontent.com/') + '/main/README.md'
    summary = {"files_scanned": 0, "findings": {}, "errors": []}
    try:
        resp = requests.get(api_url)
        summary["files_scanned"] = 1
        if resp.status_code == 200:
            findings = scan_text(resp.text)
            if findings:
                summary["findings"]["README.md"] = findings
        else:
            summary["errors"].append("Could not fetch README.md for scanning.")
    except Exception as e:
        summary["errors"].append(str(e))
    return summary

def scan_s3_bucket(bucket_name):
    # Try to list and scan files in a public or private S3 bucket (list up to 5 files)
    summary = {"files_scanned": 0, "findings": {}, "errors": []}
    try:
        try:
            import boto3
            s3 = boto3.client('s3')
            resp = s3.list_objects_v2(Bucket=bucket_name, MaxKeys=5)
            if 'Contents' not in resp:
                summary["errors"].append(f"No files found or access denied for bucket {bucket_name}.")
                return summary
            for obj in resp['Contents']:
                key = obj['Key']
                file_obj = s3.get_object(Bucket=bucket_name, Key=key)
                content = file_obj['Body'].read().decode('utf-8', errors='ignore')
                summary["files_scanned"] += 1
                file_findings = scan_text(content)
                if file_findings:
                    summary["findings"][key] = file_findings
        except ImportError:
            # Fallback to requests for public buckets
            import xml.etree.ElementTree as ET
            url = f"https://{bucket_name}.s3.amazonaws.com/"
            resp = requests.get(url)
            if resp.status_code != 200:
                summary["errors"].append(f"Could not access bucket {bucket_name}. Is it public?")
                return summary
            tree = ET.fromstring(resp.text)
            keys = [elem.text for elem in tree.findall('.//{http://s3.amazonaws.com/doc/2006-03-01/}Key')]
            for key in keys[:5]:
                file_url = f"https://{bucket_name}.s3.amazonaws.com/{key}"
                file_resp = requests.get(file_url)
                summary["files_scanned"] += 1
                if file_resp.status_code == 200:
                    file_findings = scan_text(file_resp.text)
                    if file_findings:
                        summary["findings"][key] = file_findings
                else:
                    summary["errors"].append(f"Could not fetch {key}")
        if not summary["findings"] and not summary["errors"]:
            summary["info"] = "No sensitive data found in first 5 files."
        return summary
    except Exception as e:
        summary["errors"].append(str(e))
        return summary
import re
import requests

def scan_github_repo(repo_url):
    # For demo, just fetch README.md if exists
    api_url = repo_url.replace('https://github.com/', 'https://raw.githubusercontent.com/') + '/main/README.md'
    summary = {"files_scanned": 0, "findings": {}, "errors": []}
    try:
        resp = requests.get(api_url)
        summary["files_scanned"] = 1
        if resp.status_code == 200:
            findings = scan_text(resp.text)
            if findings:
                summary["findings"]["README.md"] = findings
        else:
            summary["errors"].append("Could not fetch README.md for scanning.")
    except Exception as e:
        summary["errors"].append(str(e))
    return summary

def scan_s3_bucket(bucket_name):
    # Try to list and scan files in a public or private S3 bucket (list up to 5 files)
    summary = {"files_scanned": 0, "findings": {}, "errors": []}
    try:
        try:
            import boto3
            s3 = boto3.client('s3')
            resp = s3.list_objects_v2(Bucket=bucket_name, MaxKeys=5)
            if 'Contents' not in resp:
                summary["errors"].append(f"No files found or access denied for bucket {bucket_name}.")
                return summary
            for obj in resp['Contents']:
                key = obj['Key']
                file_obj = s3.get_object(Bucket=bucket_name, Key=key)
                content = file_obj['Body'].read().decode('utf-8', errors='ignore')
                summary["files_scanned"] += 1
                file_findings = scan_text(content)
                if file_findings:
                    summary["findings"][key] = file_findings
        except ImportError:
            # Fallback to requests for public buckets
            import xml.etree.ElementTree as ET
            url = f"https://{bucket_name}.s3.amazonaws.com/"
            resp = requests.get(url)
            if resp.status_code != 200:
                summary["errors"].append(f"Could not access bucket {bucket_name}. Is it public?")
                return summary
            tree = ET.fromstring(resp.text)
            keys = [elem.text for elem in tree.findall('.//{http://s3.amazonaws.com/doc/2006-03-01/}Key')]
            for key in keys[:5]:
                file_url = f"https://{bucket_name}.s3.amazonaws.com/{key}"
                file_resp = requests.get(file_url)
                summary["files_scanned"] += 1
                if file_resp.status_code == 200:
                    file_findings = scan_text(file_resp.text)
                    if file_findings:
                        summary["findings"][key] = file_findings
                else:
                    summary["errors"].append(f"Could not fetch {key}")
        if not summary["findings"] and not summary["errors"]:
            summary["info"] = "No sensitive data found in first 5 files."
        return summary
    except Exception as e:
        summary["errors"].append(str(e))
        return summary
import re
import requests

def scan_github_repo(repo_url):
    # For demo, just fetch README.md if exists
    api_url = repo_url.replace('https://github.com/', 'https://raw.githubusercontent.com/') + '/main/README.md'
    summary = {"files_scanned": 0, "findings": {}, "errors": []}
    try:
        resp = requests.get(api_url)
        summary["files_scanned"] = 1
        if resp.status_code == 200:
            findings = scan_text(resp.text)
            if findings:
                summary["findings"]["README.md"] = findings
        else:
            summary["errors"].append("Could not fetch README.md for scanning.")
    except Exception as e:
        summary["errors"].append(str(e))
    return summary

def scan_s3_bucket(bucket_name):
    # Try to list and scan files in a public or private S3 bucket (list up to 5 files)
    summary = {"files_scanned": 0, "findings": {}, "errors": []}
    try:
        try:
            import boto3
            s3 = boto3.client('s3')
            resp = s3.list_objects_v2(Bucket=bucket_name, MaxKeys=5)
            if 'Contents' not in resp:
                summary["errors"].append(f"No files found or access denied for bucket {bucket_name}.")
                return summary
            for obj in resp['Contents']:
                key = obj['Key']
                file_obj = s3.get_object(Bucket=bucket_name, Key=key)
                content = file_obj['Body'].read().decode('utf-8', errors='ignore')
                summary["files_scanned"] += 1
                file_findings = scan_text(content)
                if file_findings:
                    summary["findings"][key] = file_findings
        except ImportError:
            # Fallback to requests for public buckets
            import xml.etree.ElementTree as ET
            url = f"https://{bucket_name}.s3.amazonaws.com/"
            resp = requests.get(url)
            if resp.status_code != 200:
                summary["errors"].append(f"Could not access bucket {bucket_name}. Is it public?")
                return summary
            tree = ET.fromstring(resp.text)
            keys = [elem.text for elem in tree.findall('.//{http://s3.amazonaws.com/doc/2006-03-01/}Key')]
            for key in keys[:5]:
                file_url = f"https://{bucket_name}.s3.amazonaws.com/{key}"
                file_resp = requests.get(file_url)
                summary["files_scanned"] += 1
                if file_resp.status_code == 200:
                    file_findings = scan_text(file_resp.text)
                    if file_findings:
                        summary["findings"][key] = file_findings
                else:
                    summary["errors"].append(f"Could not fetch {key}")
        if not summary["findings"] and not summary["errors"]:
            summary["info"] = "No sensitive data found in first 5 files."
        return summary
    except Exception as e:
        summary["errors"].append(str(e))
        return summary

