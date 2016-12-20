import sublime, sublime_plugin, sublime_util as su

class SmallFontSizeCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        s = sublime.load_settings("Preferences.sublime-settings")
        size = s.get("small_font_size", 10)
        s.set("font_size", size)
        sublime.save_settings("Preferences.sublime-settings")

class LargeFontSizeCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        s = sublime.load_settings("Preferences.sublime-settings")
        size = s.get("large_font_size", 24)
        s.set("font_size", size)
        sublime.save_settings("Preferences.sublime-settings")
