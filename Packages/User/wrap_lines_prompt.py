import sublime, sublime_plugin

class WrapLinesPromptCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel("Width:", "", self.on_done, None, None)

    def on_done(self, text):
        self.window.active_view().run_command("wrap_lines", {"width": int(text)} )
