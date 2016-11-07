import sublime, sublime_plugin, re

class AddFrameCommand(sublime_plugin.TextCommand):
    # Add an ascii frame around selected text
    #                                +------------------+
    #     abc <suppose\n             | abc <suppose     |
    #     this text was\n       =>   | this text was    |
    #     selected> ghijkl\n         | selected> ghijkl |
    #                                +------------------+
    # The command adds one line above & below, and two 'columns' left & right
    # A selection may start and/or end in the middle of a row
    def run(self, edit):
        self.view.run_command('right_pad_spaces')
        new_sel = []
        for selection in reversed(self.view.sel()):
            region = selection
            old_a = region.a
            old_b = region.b
            lines = self.view.lines(selection)
            length = lines[0].size()
            min_indent = min(map(lambda line: re.search('[^ ]', self.view.substr(line)).start(), lines))
            new_lines = []
            new_lines.append(" " * min_indent + "+-" + "-" * (length - min_indent) + "-+")
            for line in lines:
                reg = sublime.Region(line.a + min_indent, line.b)
                new_lines.append(" " * min_indent + "| " + self.view.substr(reg) + " |")
            new_lines.append(" " * min_indent + "+-" + "-" * (length - min_indent) + "-+")
            new_text = "\n".join(new_lines) + "\n"
            new_b = old_a + len(new_text)
            _new_sel = []
            n = new_b - old_b
            for rg in reversed(new_sel):
                _new_sel.append(sublime.Region(rg.a + n, rg.b + n))
            new_sel = _new_sel
            new_sel.append(sublime.Region(old_a, new_b))
            self.view.replace(edit, region, new_text)
        self.view.set_selection(new_sel)
