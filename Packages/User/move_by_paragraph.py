import sublime, sublime_plugin

class MoveByParagraphCommand(sublime_plugin.TextCommand):
    def run(self, edit, extend = False, forward = True):
        old_a = self.view.sel()[0].a
        self.view.run_command("move_to", {"to": "hardbol", "extend": extend}) # to mimic TextPad's behaviour
        pt = self.view.sel()[0].b
        if forward:
            rg = self.view.find("\n\s*\n", pt)
            new_b = rg.b if rg else self.view.size()
        else:
            # couldn't find "find previous" command
            rgs = self.view.find_all("\n[\s]*\n")
            new_b = 0
            for rg in rgs:
                if rg.b < pt:
                    new_b = rg.b
        new_b_visible = self.view.visible_region().contains(new_b)
        #
        new_a = old_a if extend else new_b
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(new_a, new_b))
        if not new_b_visible:
            self.view.show_at_center(new_b)
