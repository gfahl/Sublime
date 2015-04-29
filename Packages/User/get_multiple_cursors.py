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

    def is_enabled(self):
        return has_bookmarks(self.view) or has_selected_lines(self.view)
