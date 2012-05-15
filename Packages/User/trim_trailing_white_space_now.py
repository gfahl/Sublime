import sublime, sublime_plugin

class TrimTrailingWhiteSpaceNow(sublime_plugin.TextCommand):
    def run(self, edit):
        trailing_white_space = self.view.find_all("[\t ]+$")
        trailing_white_space.reverse()
        for r in trailing_white_space:
            self.view.erase(edit, r)
