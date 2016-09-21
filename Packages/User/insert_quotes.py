import sublime, sublime_plugin, re, string

class InsertQuotesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if any(rg.empty() for rg in self.view.sel()):
            self.view.window().run_command("find_under_expand")
        for rg in reversed(self.view.sel()):
            s = self.view.substr(rg)
            if s[0] == "'" and s[-1] == "'":
                s = '"' + s[1:-1] + '"'
            elif s[0] == '"' and s[-1] == '"':
                s = "_" + s[1:-1] + "_"
            elif s[0] == "_" and s[-1] == "_":
                s = "*" + s[1:-1] + "*"
            elif s[0] == "*" and s[-1] == "*":
                s = s[1:-1]
            else:
                s = "'" + s + "'"
            self.view.replace(edit, rg, s)
