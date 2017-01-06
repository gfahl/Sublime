import sublime, sublime_plugin, sublime_util as su

print "Applying platform-specific settings (platform: '%s')" % (sublime.platform())
s = sublime.load_settings("Preferences.sublime-settings")
if sublime.platform() == 'windows':
    s.set("font_face", "Consolas")
    s.set("font_size", 11)
    s.set("small_font_size", 10)
    s.set("large_font_size", 24)
elif sublime.platform() == 'osx':
    s.set("font_face", "Inconsolata")
    s.set("font_size", 15)
    s.set("small_font_size", 15)
    s.set("large_font_size", 22)
elif sublime.platform() == 'linux':
    pass
else:
    print 'Warning: Unexpected platform'
sublime.save_settings("Preferences.sublime-settings")
