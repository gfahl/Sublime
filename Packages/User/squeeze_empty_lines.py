import sublime, sublime_plugin, re

class SqueezeEmptyLinesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        new_sel = []
        for region in self.view.sel():
            old_text = self.view.substr(region)
            regex = re.compile('\n[\n\s]*\n', flags=re.MULTILINE)
            new_text = re.sub(regex, '\n\n', old_text)
            if self.view.substr(region.begin() - 1) == '\n' and new_text[0:2] == '\n\n':
                new_text = new_text[1:]
            self.view.replace(edit, region, new_text)
