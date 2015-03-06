import sublime, sublime_plugin, datetime

class PasteDateCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for s in self.view.sel():
            self.view.replace(edit, s, str(datetime.date.today()))
