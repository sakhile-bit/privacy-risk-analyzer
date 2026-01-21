import os
from scanner_core import scan_text

def scan_local_folder(folder_path):
    summary = {"files_scanned": 0, "findings": {}, "errors": []}
    for root, dirs, files in os.walk(folder_path):
        for fname in files:
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                findings = scan_text(content)
                summary["files_scanned"] += 1
                if findings:
                    summary["findings"][fpath] = findings
            except Exception as e:
                summary["errors"].append(f"{fpath}: {e}")
    if not summary["findings"] and not summary["errors"]:
        summary["info"] = "No sensitive data found."
    return summary
