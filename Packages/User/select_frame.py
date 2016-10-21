import sublime, sublime_plugin, re

class SelectFrameCommand(sublime_plugin.TextCommand):
    # Selects the smallest ascii frame that contains the selection
    def run(self, edit):
        v = self.view
        last_row = v.rowcol(v.size())[0]
        directions = list('WNES')

        # initial frame boundary
        orig = {
            'W': min(map(lambda rg: v.rowcol(rg.begin())[1], v.sel())),
            'N': v.rowcol(v.sel()[0].begin())[0],
            'E': max(map(lambda rg: v.rowcol(rg.end())[1], v.sel())),
            'S': v.rowcol(v.sel()[-1].begin())[0]
            }

        # the lowest and highest row/column number we will look for a frame at
        min_col = 0
        max_col = min(map(lambda rg: v.rowcol(v.line(rg).b)[1], v.sel()))
        min_row = next(
            (row for row in range(orig['N'], 0, -1) if
                v.rowcol(v.line(v.text_point(row, 0)).b)[1] < orig['E']),
            -1
            ) + 1
        max_row = next(
            (row for row in range(orig['S'], last_row, 1) if
                v.rowcol(v.line(v.text_point(row, 0)).b)[1] < orig['E']),
            last_row + 1
            ) - 1

        best = None
        for expand_direction in directions:
            cand = dict(orig) # candidate frame
            if expand_direction == 'W' or expand_direction == 'N':
                cand[expand_direction] -= 1
            else:
                cand[expand_direction] += 1
            if cand['W'] < min_col or cand['N'] < min_row or cand['E'] > max_col or cand['S'] > max_row:
                continue

            failure = False
            direction_queue = list(directions)
            while not failure and not self.is_frame(cand):
                search_direction = direction_queue[0]
                direction_queue = direction_queue[1:] + direction_queue[:1]
                if search_direction == 'W':
                    while cand['W'] >= min_col and not self.is_line(cand, 'W'):
                        cand['W'] -= 1
                elif search_direction == 'N':
                    while cand['N'] >= min_row and not self.is_line(cand, 'N'):
                        cand['N'] -= 1
                elif search_direction == 'E':
                    while cand['E'] <= max_col and not self.is_line(cand, 'E'):
                        cand['E'] += 1
                elif search_direction == 'S':
                    while cand['S'] <= max_row and not self.is_line(cand, 'S'):
                        cand['S'] += 1
                failure = not self.is_line(cand, search_direction)

            if not failure:
                if best == None:
                    best = cand
                else:
                    size_best = (best['S'] - best['N']) * (best['E'] - best['W'])
                    size_cand = (cand['S'] - cand['N']) * (cand['E'] - cand['W'])
                    if size_cand < size_best:
                        best = cand

        if best:
            v.sel().clear()
            for row in range(best['N'], best['S'] + 1, 1):
                a = v.text_point(row, best['W'])
                b = v.text_point(row, best['E'])
                v.sel().add(sublime.Region(a, b))

    def is_frame(self, rect):
        return (
            self.is_line(rect, 'W') and
            self.is_line(rect, 'N') and
            self.is_line(rect, 'E') and
            self.is_line(rect, 'S')
            )

    def is_line(self, rect, side):
        if side == 'W':
            return self.is_vertical_line(rect['W'], rect['N'], rect['S'])
        elif side == 'E':
            return self.is_vertical_line(rect['E'] - 1, rect['N'], rect['S'])
        elif side == 'N':
            return self.is_horizontal_line(rect['N'], rect['W'], rect['E'] - 1)
        elif side == 'S':
            return self.is_horizontal_line(rect['S'], rect['W'], rect['E'] - 1)
        else:
            raise Exception('Unexpected side: %s' % side)

    def is_horizontal_line(self, row, left_col, right_col):
        v = self.view
        s = ''
        col = left_col
        while col <= right_col:
            s += v.substr(v.text_point(row, col))
            col += 1
        return re.match('[+-]+$', s)

    def is_vertical_line(self, col, top_row, bottom_row):
        v = self.view
        s = ''
        row = top_row
        while row <= bottom_row:
            s += v.substr(v.text_point(row, col))
            row += 1
        return re.match('[+|]+$', s)
