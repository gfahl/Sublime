import sublime, sublime_plugin, re, string

class ToggleCamelSnakeCaseCommand(sublime_plugin.TextCommand):
	# changes selection as follows:
	# "foo fie fum" => "foo_fie_fum" => "FooFieFum" => "foo fie fum" etc.
    def run(self, edit):
        for rg in reversed(self.view.sel()):
            s = self.view.substr(rg)
            # if re.search("_", s):
            if s.find("_") >= 0:
                s = "".join(map(string.capwords, s.split("_")))
            elif s.find(" ") >= 0:
                s = s.replace(" ", "_")
            else:
                s = s[0].upper() + s[1:] # make fooFieFum behave like FooFieFum
            	s = " ".join(map(string.lower, re.findall("[A-Z][a-z]*", s)))
            self.view.replace(edit, rg, s)
