import sublime, sublime_plugin

class PasteLoremIpsumShortCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for s in self.view.sel():
            self.view.replace(edit, s, 'Lorem ipsum dolor sit amet')

class PasteLoremIpsumLongCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for s in self.view.sel():
            self.view.replace(edit, s, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.')
