import sublime, sublime_plugin, sublime_util as su

class DecreaseFontSizeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        v = self.view
        v.settings().set("font_size", v.settings().get("font_size") / 1.1)

class IncreaseFontSizeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        v = self.view
        v.settings().set("font_size", v.settings().get("font_size") * 1.1)

class ResetFontCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        v = self.view
        s = sublime.load_settings("Font.sublime-settings")
        if sublime.platform() == "windows" or sublime.platform() == "osx":
            v.settings().set("font_face", s.get("face")[sublime.platform()])
            v.settings().set("font_size", s.get("size")[sublime.platform()])
        if v.score_selector(0, "text.japanese") > 0:
            v.settings().set("font_size", v.settings().get("font_size") * s.get("factor")["text.japanese"])

class FontEventListener(sublime_plugin.EventListener):
    def main(self, view):
        if view.settings().get('is_widget'): return
        if view.settings().get("font_initialized"): return
        view.run_command('reset_font')
        view.settings().set("font_initialized", True)

    def on_activated(self, view):
        self.main(view)

    def on_load(self, view):
        self.main(view)

    def on_new(self, view):
        self.main(view)
