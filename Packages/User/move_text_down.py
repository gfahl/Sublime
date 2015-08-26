import sublime, sublime_plugin

class MoveTextDownCommand(sublime_plugin.TextCommand):
    # Meant to be used for text on a 'space background'
    # Move all selections one row down
    # Assumes that the line below a selection is long enough
	# +-------+    +-------+
	# | <def> |    |  abc  |
	# | <ghi> | => | <def> |
	# |  abc  |    | <ghi> |
	# +-------+    +-------+
    def run(self, edit):
        new_sel = []
        v = self.view
        for r in reversed(v.sel()):
            text = v.substr(r)
            rc1 = v.rowcol(r.begin())
            rc2 = v.rowcol(r.end())
            p1 = v.text_point(rc1[0] + 1, rc1[1])
            p2 = v.text_point(rc2[0] + 1, rc2[1])
            region_below = sublime.Region(p1, p2)
            text_below = v.substr(region_below)
            v.replace(edit, region_below, text)
            v.replace(edit, r, text_below)
            new_sel.append(region_below)
        v.sel().clear()
        for rg in new_sel:
            v.sel().add(rg)
