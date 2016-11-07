import sublime, sublime_plugin, re

class ReverseSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        v = self.view
        new_sels = []
        for s in v.sel():
            new_sels.append(sublime.Region(s.b, s.a))
        v.sel().clear()
        for s in new_sels:
            v.sel().add(s)
