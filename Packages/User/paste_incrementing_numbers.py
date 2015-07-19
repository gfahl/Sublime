import sublime, sublime_plugin

class PasteIncrementingNumbersCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        regions = self.view.sel()
        n = len(regions)
        for rg in reversed(regions):
            self.view.replace(edit, rg, str(n))
            n -= 1
