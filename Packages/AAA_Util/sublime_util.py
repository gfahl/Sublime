import sublime, re

def col(self, text_point):
    return self.rowcol(text_point)[1]

def max_col(self, row):
    if row < 0 or row > self.max_row():
        return 0
    else:
        return self.col(self.line(self.text_point(row, 0)).end())

def max_row(self):
    return self.rowcol(self.size())[0]

def row(self, text_point):
    return self.rowcol(text_point)[0]

def rowcol_exists(self, row, col):
    return self.rowcol(self.text_point(row, col)) == (row, col)

def set_selection(self, regions):
    self.sel().clear()
    for rg in regions:
        self.sel().add(rg)

sublime.View.rowcol_exists = rowcol_exists
sublime.View.max_col = max_col
sublime.View.max_row = max_row
sublime.View.row = row
sublime.View.col = col
sublime.View.set_selection = set_selection

def to_snake_case(s):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
