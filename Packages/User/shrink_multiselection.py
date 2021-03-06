import sublime, sublime_plugin, sublime_util as su

class ShrinkMultiselectionCommand(sublime_plugin.TextCommand):
    def run(self, edit, first):
        v = self.view
        new_sel = []
        if first:
            rng = range(1, len(v.sel()), 1)
        else:
            rng = range(0, len(v.sel()) - 1, 1)
        for i in rng:
            new_sel.append(v.sel()[i])
        v.set_selection(new_sel)
