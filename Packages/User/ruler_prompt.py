import sublime, sublime_plugin, sublime_util as su

class RulerPromptCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel("Column:", "", self.on_done, None, None)

    def on_done(self, text):
        columns = map(int, text.split(","))
        self.window.active_view().run_command("set_setting", {"setting": "rulers", "value": columns} )
