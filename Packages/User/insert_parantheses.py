import sublime, sublime_plugin, re, string

class InsertParenthesesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for rg in reversed(self.view.sel()):
            s = self.view.substr(rg)
            if s[0] == "(" and s[-1] == ")":
                s = "[" + s[1:-1] + "]"
            elif s[0] == "[" and s[-1] == "]":
                s = "{" + s[1:-1] + "}"
            elif s[0] == "{" and s[-1] == "}":
                s = "<" + s[1:-1] + ">"
            elif s[0] == "<" and s[-1] == ">":
                s = s[1:-1]
            else:
                s = "(" + s + ")"
            self.view.replace(edit, rg, s)