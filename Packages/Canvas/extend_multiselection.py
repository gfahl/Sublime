import sublime, sublime_plugin, sublime_util as su

class ExtendMultiselectionCommand(sublime_plugin.TextCommand):
    def run(self, edit, forward):
        v = self.view
        if forward:
            rg = v.sel()[-1]
            start_row, start_col = v.rowcol(rg.a)
            end_row, end_col = v.rowcol(rg.b)
            a = v.text_point(start_row + 1, start_col)
            b = v.text_point(end_row + 1, end_col)
        else:
            rg = v.sel()[0]
            start_row, start_col = v.rowcol(rg.a)
            end_row, end_col = v.rowcol(rg.b)
            a = v.text_point(start_row - 1, start_col)
            b = v.text_point(end_row - 1, end_col)
        v.sel().add(sublime.Region(a, b))
