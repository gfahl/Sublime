import sublime

def col(self, text_point):
	return self.rowcol(text_point)[1]

def row(self, text_point):
	return self.rowcol(text_point)[0]

def rowcol_exists(self, row, col):
    return self.rowcol(self.text_point(row, col)) == (row, col)

sublime.View.rowcol_exists = rowcol_exists
sublime.View.row = row
sublime.View.col = col
