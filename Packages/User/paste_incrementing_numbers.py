import sublime, sublime_plugin, re

def n_to_col(n):
    quotient, remainder = divmod(n - 1, 26)
    return '' if n == 0 else n_to_col(quotient) + chr(ord('a') + remainder)

def col_to_n(col):
    return 0 if col == '' else col_to_n(col[:-1]) * 26 + ord(col[-1]) - ord('a') + 1

class PasteIncrementingNumbersCommand(sublime_plugin.TextCommand):
    def run(self, edit, start = '1'):
        regions = self.view.sel()
        if re.match('[0-9]+$', start):
            n = int(start) + len(regions) - 1
            for rg in reversed(regions):
                self.view.replace(edit, rg, str(n))
                n -= 1
        elif re.match('[a-z]+$', start):
            n = col_to_n(start) + len(regions) - 1
            for rg in reversed(regions):
                self.view.replace(edit, rg, n_to_col(n))
                n -= 1

class PasteEnumerationCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel("Start:", "", self.on_done, None, None)

    def on_done(self, text):
        self.window.active_view().run_command("paste_incrementing_numbers", {"start": text} )
