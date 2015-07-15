import sublime, sublime_plugin

def has_bookmarks(view):
    return len(view.get_regions("bookmarks")) > 1

def has_selected_lines(view):
    return len(view.sel()) == 1 and len(view.lines(view.sel()[0])) > 1

class GetMultipleCursorsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if has_selected_lines(self.view):
            self.view.run_command('split_selection_into_lines')
        elif has_bookmarks(self.view):
            self.view.run_command('select_all_bookmarks')
        else:
            new_sel = []
            for rg in self.view.sel():
                if rg.a != rg.b:
                    pos = rg.begin()
                    while pos < rg.end():
                        new_sel.append(sublime.Region(pos, pos + 1))
                        pos = pos + 1
                else:
                    new_sel.append(rg)
            self.view.sel().clear()
            for rg in new_sel:
                self.view.sel().add(rg)

    def is_enabled(self):
        return True
