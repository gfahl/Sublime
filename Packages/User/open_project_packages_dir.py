import sublime, sublime_plugin, sublime_util as su
import re

class OpenProjectPackagesDirCommand(sublime_plugin.WindowCommand):
    def run(self):
        folder = next((s for s in self.window.folders() if re.search('[/\\\\]Sublime$', s)), None)
        if folder:
            self.window.run_command('open_dir', {'dir': folder + '/Packages', 'file': 'User'})
        else:
            sublime.status_message('Could not open Project/Packages folder')
