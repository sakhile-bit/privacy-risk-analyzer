from flask import Flask, render_template_string, request
from scanner_core import scan_github_repo, scan_s3_bucket
from folder_scanner import scan_local_folder

app = Flask(__name__)

TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>Privacy Risk Analyzer</title></head>
<body>
<h1>Privacy Risk Analyzer</h1>
<form method="post">
    <label>GitHub Repo URL: <input name="repo_url"></label>
    <button type="submit" name="action" value="github">Scan GitHub</button><br><br>
    <label>S3 Bucket Name: <input name="bucket_name"></label>
    <button type="submit" name="action" value="s3">Scan S3</button><br><br>
    <label>Local Folder: <input name="folder_path"></label>
    <button type="submit" name="action" value="local">Scan Local</button>
</form>
{% if summary %}
  <h2>Scan Summary</h2>
  <ul>
    <li><b>Files Scanned:</b> {{ summary.files_scanned }}</li>
    {% if summary.info %}<li><b>Info:</b> {{ summary.info }}</li>{% endif %}
    {% if summary.errors and summary.errors|length > 0 %}
      <li><b>Errors:</b>
        <ul>
        {% for err in summary.errors %}
          <li>{{ err }}</li>
        {% endfor %}
        </ul>
      </li>
    {% endif %}
  </ul>
  {% if summary.findings and summary.findings|length > 0 %}
    <h2>Findings</h2>
    <ul>
    {% for fname, fdata in summary.findings.items() %}
      <li><b>{{ fname }}</b>
        <ul>
        {% for k, v in fdata.items() %}
          <li>{{ k }}: {{ v }}</li>
        {% endfor %}
        </ul>
      </li>
    {% endfor %}
    </ul>
  {% else %}
    <p>No sensitive data found.</p>
  {% endif %}
{% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
  summary = None
  error = None
  if request.method == 'POST':
    action = request.form['action']
    if action == 'github':
      repo_url = request.form['repo_url'].strip()
      if not repo_url or not repo_url.startswith('http'):
        summary = {"files_scanned": 0, "findings": {}, "errors": ["Please enter a valid GitHub repository URL."]}
      else:
        summary = scan_github_repo(repo_url)
    elif action == 's3':
      bucket_name = request.form['bucket_name'].strip()
      if not bucket_name:
        summary = {"files_scanned": 0, "findings": {}, "errors": ["Please enter a valid S3 bucket name."]}
      else:
        summary = scan_s3_bucket(bucket_name)
    elif action == 'local':
      folder_path = request.form['folder_path'].strip()
      import os
      if not folder_path or not os.path.isdir(folder_path):
        summary = {"files_scanned": 0, "findings": {}, "errors": ["Please enter a valid local folder path that exists."]}
      else:
        summary = scan_local_folder(folder_path)
  return render_template_string(TEMPLATE, summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
