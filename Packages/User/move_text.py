import sublime, sublime_plugin

class MoveTextCommand(sublime_plugin.TextCommand):
    def is_enabled(self):
        return next((r for r in self.view.sel() if self.movable(r)), None)

    def move(self, edit, delta):
        for r in self.view.sel():
            if not self.movable(r): continue
            self.view.sel().subtract(r)
            s = self.view.substr(r)
            self.view.erase(edit, r)
            self.view.insert(edit, r.begin() + delta, s)
            self.view.sel().add(sublime.Region(r.a + delta, r.b + delta))

class MoveTextLeftCommand(MoveTextCommand):
    def run(self, edit):
        self.move(edit, -1)

    def movable(self, region):
        return not region.empty() and region.begin() > 0

class MoveTextRightCommand(MoveTextCommand):
    def run(self, edit):
        self.move(edit, 1)

    def movable(self, region):
        return not region.empty() and region.end() < self.view.size()
