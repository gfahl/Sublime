import sublime, sublime_plugin

class PasteIncrementingNumbersCommand(sublime_plugin.TextCommand):
    def run(self, edit, start = 1):
        regions = self.view.sel()
        n = start + len(regions) - 1
        for rg in reversed(regions):
            self.view.replace(edit, rg, str(n))
            n -= 1

class PasteIncrementingNumbersInteractiveCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel("Start:", "", self.on_done, None, None)

    def on_done(self, text):
        self.window.active_view().run_command("paste_incrementing_numbers", {"start": int(text)} )
