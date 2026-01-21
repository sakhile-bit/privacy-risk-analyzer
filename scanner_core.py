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

def scan_text(text):
    patterns = {
        'Email': r'[\w\.-]+@[\w\.-]+',
        'AWS Access Key': r'AKIA[0-9A-Z]{16}',
        'AWS Secret Key': r'(?<![A-Z0-9])[A-Za-z0-9/+=]{40}(?![A-Z0-9])',
        'Google API Key': r'AIza[0-9A-Za-z\-_]{35}',
        'Slack Token': r'xox[baprs]-([0-9a-zA-Z]{10,48})?',
        'Credit Card': r'\b(?:\d[ -]*?){13,16}\b',
        'US SSN': r'\b\d{3}-\d{2}-\d{4}\b',
        'IPv4 Address': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
        'Private Key': r'-----BEGIN PRIVATE KEY-----[\s\S]+?-----END PRIVATE KEY-----',
        'Password in Text': r'password\s*[:=]\s*[^\s]+',
        'Bearer Token': r'Bearer [A-Za-z0-9\-\._~\+\/]+=*',
        'Generic Secret': r'secret\s*[:=]\s*[^\s]+',
    }
    findings = {}
    for name, pat in patterns.items():
        matches = re.findall(pat, text, re.IGNORECASE)
        if matches:
            findings[name] = matches
    try:
        from plugin_manager import plugin_manager
        plugin_findings = plugin_manager.run_plugins(text)
        if plugin_findings:
            findings['Plugins'] = plugin_findings
    except Exception as e:
        findings['Plugins'] = f"Plugin error: {e}"
    return findings
