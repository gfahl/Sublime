import sublime, sublime_plugin, sublime_util as su

class MoveTextUpCommand(sublime_plugin.TextCommand):
    # Meant to be used for text on a 'space background'
    # Move all selections one row up
    # Assumes that the line above a selection is long enough
    # +-------+    +-------+
    # |  abc  |    | <def> |
    # | <def> | => | <ghi> |
    # | <ghi> |    |  abc  |
    # +-------+    +-------+
    def run(self, edit):
        new_sel = []
        v = self.view
        for r in v.sel():
            text = v.substr(r)
            rc1 = v.rowcol(r.begin())
            rc2 = v.rowcol(r.end())
            p1 = v.text_point(rc1[0] - 1, rc1[1])
            p2 = v.text_point(rc2[0] - 1, rc2[1])
            region_above = sublime.Region(p1, p2)
            text_above = v.substr(region_above)
            v.replace(edit, region_above, text)
            v.replace(edit, r, text_above)
            new_sel.append(region_above)
        v.set_selection(new_sel)
