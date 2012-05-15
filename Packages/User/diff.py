import sublime, sublime_plugin, subprocess

class DiffCommand(sublime_plugin.WindowCommand):
	def run(self):
		f2 = self.window.active_view().file_name()
		self.window.run_command("next_view_in_stack")
		f1 = self.window.active_view().file_name()
		self.window.run_command("prev_view_in_stack")
		subprocess.Popen(["TortoiseMerge.exe", f1, f2])

class DiffCheckedInCommand(sublime_plugin.WindowCommand):
	def run(self):
		f = self.window.active_view().file_name()
		subprocess.Popen('TortoiseProc.exe /command:diff /path:"%s"' % f)
