# Example plugin: Detect TODO comments

def detect(text):
    import re
    todos = re.findall(r'TODO[:\s].*', text)
    if todos:
        return {'TODOs': todos}
    return None
