import sublime, sublime_plugin

class MoveTextUpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print 'hello'
