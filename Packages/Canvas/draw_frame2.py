import sublime, sublime_plugin, re

class DrawFrame2Command(sublime_plugin.TextCommand):
    # Draw an ascii frame on the edges of selected text
    # Pre-requisite: a rectangular-shaped multi-selection
    #   the selections are on consecutive lines
    #   the selections have the same start- and end-position within the lines
    # The command does not add any new lines or columns
    # Height of one line and/or width of one column is allowed
    # If a drawn line passes an orthogonal line, an intersection is drawn
    #
    #   abc <suppose      > jkl        abc +-------------+ jkl
    #   def <this text was> mno   =>   def !this text was! mno
    #   ghi <selected     > pqr        ghi +-------------+ pqr
    def run(self, edit):
        rows_a = [self.view.rowcol(r.a)[0] for r in self.view.sel()]
        rows_b = [self.view.rowcol(r.b)[0] for r in self.view.sel()]
        cols_a = [self.view.rowcol(r.a)[1] for r in self.view.sel()]
        cols_b = [self.view.rowcol(r.b)[1] for r in self.view.sel()]
        if rows_a != rows_b: return
        if rows_a != range(rows_a[0], rows_a[-1] + 1): return
        if len(set(cols_a)) != 1: return
        if len(set(cols_b)) != 1: return
        if cols_a == cols_b: return
        for i in [0, -1]:
            region = self.view.sel()[i]
            old_text = self.view.substr(region)
            new_text = re.sub("\!", "+", old_text)
            new_text = re.sub("[^+]", "-", new_text)
            new_text = "+" + new_text[1:]
            new_text = new_text[:-1] + "+"
            self.view.replace(edit, region, new_text)
        if len(self.view.sel()) > 2:
            for i in range(1, len(self.view.sel()) - 1):
                region = self.view.sel()[i]
                old_text = self.view.substr(region)
                new_text = old_text
                new_text = ("+" if old_text[0] == "+" or old_text[0] == "-" else "!") + new_text[1:]
                new_text = new_text[:-1] + ("+" if old_text[0] == "+" or old_text[0] == "-" else "!")
                self.view.replace(edit, region, new_text)
