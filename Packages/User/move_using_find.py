import sublime, sublime_plugin

class PromptMoveUsingFindCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.window.show_input_panel("Find:", "", self.on_done, None, None)

    def on_done(self, text):
        self.window.active_view().run_command("move_using_find", {"regex": text} )

class MoveUsingFindCommand(sublime_plugin.TextCommand):

    def run(self, edit, regex):
        new_sel = []
        for rg in self.view.sel():
            new_rg = self.view.find(regex, rg.a)
            new_sel.append(new_rg)
        self.view.sel().clear()
        for rg in new_sel:
            self.view.sel().add(rg)
