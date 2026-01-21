import importlib.util
import os

PLUGIN_FOLDER = os.path.join(os.path.dirname(__file__), 'plugins')

class PluginManager:
    def __init__(self):
        self.plugins = []
        self.load_plugins()

    def load_plugins(self):
        if not os.path.exists(PLUGIN_FOLDER):
            os.makedirs(PLUGIN_FOLDER)
        for fname in os.listdir(PLUGIN_FOLDER):
            if fname.endswith('.py'):
                path = os.path.join(PLUGIN_FOLDER, fname)
                spec = importlib.util.spec_from_file_location(fname[:-3], path)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                if hasattr(mod, 'detect'):
                    self.plugins.append(mod)

    def run_plugins(self, text):
        findings = {}
        for plugin in self.plugins:
            try:
                result = plugin.detect(text)
                if result:
                    findings[plugin.__name__] = result
            except Exception as e:
                findings[plugin.__name__] = f"Error: {e}"
        return findings

plugin_manager = PluginManager()
