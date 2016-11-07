import sublime

def col(self, text_point):
	return self.rowcol(text_point)[1]

def row(self, text_point):
	return self.rowcol(text_point)[0]

def rowcol_exists(self, row, col):
    return self.rowcol(self.text_point(row, col)) == (row, col)

def set_selection(self, regions):
	self.sel().clear()
	for rg in regions:
	    self.sel().add(rg)

sublime.View.rowcol_exists = rowcol_exists
sublime.View.row = row
sublime.View.col = col
sublime.View.set_selection = set_selection
