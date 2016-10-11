import sublime, sublime_plugin, re

class ShowPropertiesCommand(sublime_plugin.WindowCommand):
    def run(self):
        v = self.window.active_view()
        s = ""
        m = re.match('(.*)[/\\\\](.*)', v.file_name())
        s += "Filename: %s\n" % m.group(2)
        s += "Directory: %s\n" % m.group(1)
        s += "Encoding: %s\n" % v.encoding()
        s += "Tab Size: %s\n" % v.settings().get('tab_size')
        s += "Indentation: %s\n" % ("Spaces" if v.settings().get('translate_tabs_to_spaces') else "Tabs")
        s += "Size: %d characters\n" % v.size()
        s += "Line Endings: %s\n" % v.line_endings()
        s += "Syntax file: %s\n" % v.settings().get('syntax')
        s += "Font: %s %dpt\n" % (v.settings().get('font_face'), v.settings().get('font_size'))
        sublime.message_dialog(s)
        print s
