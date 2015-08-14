import sublime, sublime_plugin

class MoveByParagraphCommand(sublime_plugin.TextCommand):
    def run(self, edit, extend = False, forward = True):
        new_sel = []
        any_new_b_visible = False
        fallback_center_pt = None

        for rg in self.view.sel():
            old_a = rg.a
            old_b = rg.b
            pt = self.view.line(rg.b).begin() # to mimic TextPad's behaviour
            if forward:
                _rg = self.view.find("\n\s*\n", pt)
                new_b = _rg.b if _rg else self.view.size()
            else:
                # couldn't find "find previous" command
                _rgs = self.view.find_all("\n[\s]*\n")
                new_b = 0
                for _rg in _rgs:
                    if _rg.b < pt:
                        new_b = _rg.b
            if self.view.visible_region().contains(old_b):
                fallback_center_pt = new_b
            any_new_b_visible = any_new_b_visible or self.view.visible_region().contains(new_b)
            new_a = old_a if extend else new_b
            new_sel.append(sublime.Region(new_a, new_b))
        self.view.sel().clear()
        for rg in new_sel:
            self.view.sel().add(rg)
        if not any_new_b_visible and fallback_center_pt != None:
            self.view.show_at_center(fallback_center_pt)
