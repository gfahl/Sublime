import sublime, sublime_plugin

class CopyFilenameCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # self.view.run_command("copy_path")
        print self.view.file_name()
