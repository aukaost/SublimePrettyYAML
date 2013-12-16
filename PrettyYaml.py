import sublime
import sublime_plugin
import decimal
try:
    from . import yaml
except (ImportError, ValueError):
    import yaml

s = sublime.load_settings("Pretty YAML.sublime-settings")

class PrettyyamlCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        """ Pretty print YAML """
        for region in self.view.sel():

            selected_entire_file = False

            # If no selection, use the entire file as the selection
            if region.empty() and s.get("use_entire_file_if_no_selection", True):
                selection = sublime.Region(0, self.view.size())
                selected_entire_file = True
            else:
                selection = region

            try:
                obj = yaml.load(self.view.substr(selection))
                self.view.replace(edit, selection, yaml.dump(obj, **s.get("dumper_args")))

                if selected_entire_file:
                    self.change_syntax()

            except Exception:
                import sys
                exc = sys.exc_info()[1]
                sublime.status_message(str(exc))

    def change_syntax(self):        
        if "Plain text" in self.view.settings().get('syntax'):
            self.view.set_syntax_file("Packages/YAML/YAML.tmLanguage")


def plugin_loaded():
    global s
    s = sublime.load_settings("Pretty YAML.sublime-settings")
