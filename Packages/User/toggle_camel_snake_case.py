import sublime, sublime_plugin, re, string

class ToggleCamelSnakeCaseCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for rg in reversed(self.view.sel()):
            s = self.view.substr(rg)
            # if re.search("_", s):
            if s.find("_") >= 0:
                s = "".join(map(string.capwords, s.split("_")))
            else:
                s = "_".join(map(string.lower, re.findall("[A-Z][a-z]*", s)))
            self.view.replace(edit, rg, s)
