import sublime, sublime_plugin, re, time

def rowcol_exists(v, row, col):
    return v.rowcol(v.text_point(row, col)) == (row, col)

class Square:
    directions = tuple('WNES')

    def __init__(self, v, pos_as_tuple):
        self.v = v
        self.pos = {
            'W': pos_as_tuple[0],
            'N': pos_as_tuple[1],
            'E': pos_as_tuple[2],
            'S': pos_as_tuple[3]
            }

    @classmethod
    def from_selection(klass, v):
        left = min(map(lambda rg: v.rowcol(rg.begin())[1], v.sel()))
        top = v.rowcol(v.sel()[0].begin())[0]
        right = max(map(lambda rg: v.rowcol(rg.end())[1], v.sel()))
        bottom = v.rowcol(v.sel()[-1].end())[0]
        return klass(v, (left, top, right, bottom))

    def __str__(self):
        return "<Square: (%d, %d) (%d, %d)>" % (self.pos_as_tuple())

    def copy(self):
        return Square(self.v, self.pos_as_tuple())

    def expand(self, direction):
        if direction not in Square.directions:
            raise Exception('Unexpected direction: %s' % direction)
        delta = -1 if direction == 'W' or direction == 'N' else 1
        self.pos[direction] += delta
        return self

    def is_frame(self):
        return (
            self.is_line('W') and
            self.is_line('N') and
            self.is_line('E') and
            self.is_line('S')
            )

    def is_horizontal_line(self, row, left_col, right_col):
        s = ''
        col = left_col
        while col <= right_col:
            s += self.v.substr(self.v.text_point(row, col))
            col += 1
        return re.match('[+-]+$', s)

    def is_line(self, side):
        if side == 'W':
            return self.is_vertical_line(self.pos['W'], self.pos['N'], self.pos['S'])
        elif side == 'E':
            return self.is_vertical_line(self.pos['E'] - 1, self.pos['N'], self.pos['S'])
        elif side == 'N':
            return self.is_horizontal_line(self.pos['N'], self.pos['W'], self.pos['E'] - 1)
        elif side == 'S':
            return self.is_horizontal_line(self.pos['S'], self.pos['W'], self.pos['E'] - 1)
        else:
            raise Exception('Unexpected side: %s' % side)

    def is_valid(self):
        return (
            rowcol_exists(self.v, self.pos['N'], self.pos['W']) and
            rowcol_exists(self.v, self.pos['N'], self.pos['E']) and
            rowcol_exists(self.v, self.pos['S'], self.pos['W']) and
            rowcol_exists(self.v, self.pos['S'], self.pos['E'])
            )

    def is_vertical_line(self, col, top_row, bottom_row):
        s = ''
        row = top_row
        while row <= bottom_row:
            s += self.v.substr(self.v.text_point(row, col))
            row += 1
        return re.match('[+|]+$', s)

    def pos_as_tuple(self):
        return (self.pos['W'], self.pos['N'], self.pos['E'], self.pos['S'])

    def height(self):
        return self.pos['S'] - self.pos['N'] + 1

    def width(self):
        return self.pos['E'] - self.pos['W']

    def size(self):
        return self.height() * self.width()

    def use_as_selection(self):
        self.v.sel().clear()
        for row in range(self.pos['N'], self.pos['S'] + 1, 1):
            a = self.v.text_point(row, self.pos['W'])
            b = self.v.text_point(row, self.pos['E'])
            self.v.sel().add(sublime.Region(a, b))

class SelectFrameCommand(sublime_plugin.TextCommand):
    def __init__(self, v):
        sublime_plugin.TextCommand.__init__(self, v)
        self.last_invocation_time = 0

    def run(self, edit):
        v = self.view

        now = time.time()
        elapsed_time = now - self.last_invocation_time
        self.last_invocation_time = now

        if v.command_history(0)[0] == 'select_frame' or elapsed_time < 1:
            # Sublime's command history doesn't immediately record a new command
            # Unless we look at elapsed time too, rapid consecutive calls do not work
            self.ix += 1
        else:
            self.original_selection = [rg for rg in v.sel()]
            #
            v.sel().clear()
            for rg in self.original_selection:
                # make sure correct frame is selected when selection width = 0
                v.sel().add(sublime.Region(rg.a - 1, rg.a + 1) if rg.empty() else rg)
            #
            self.found_frames = []
                # used for avoiding recursion down branches that have already been tried
            self.get_frames(Square.from_selection(v))
            self.found_frames = filter(lambda f: f.height() >= 3 and f.width() >= 3, self.found_frames)
            self.found_frames.sort(lambda x, y: cmp(x.size(), y.size()))
            self.ix = 0

        if self.ix == len(self.found_frames):
            v.sel().clear()
            for rg in self.original_selection:
                v.sel().add(rg)
            sublime.status_message(
                "no frames found" if self.found_frames == [] else "original selection")
            self.ix = -1
        else:
            self.found_frames[self.ix].use_as_selection()
            sublime.status_message("frame %d of %d" % (self.ix + 1, len(self.found_frames)))

    def frame_already_found(self, cand):
        return next((f for f in self.found_frames if f.pos_as_tuple() == cand.pos_as_tuple()), None)

    def get_frames(self, square):
        # returns all frames which contain <square> and are bigger than <square>
        return (
            self.get_frames0(square.copy().expand('W')) +
            self.get_frames0(square.copy().expand('N')) +
            self.get_frames0(square.copy().expand('E')) +
            self.get_frames0(square.copy().expand('S'))
            )

    def get_frames0(self, square):
        # returns all frames which contain <square> and are bigger than or equal to <square>
        if not square.is_valid(): return []

        failure = False
        direction_queue = list(Square.directions)
        while not failure and not square.is_frame():
            search_direction = direction_queue[0]
            direction_queue = direction_queue[1:] + direction_queue[:1]
            while square.is_valid() and not square.is_line(search_direction):
                square.expand(search_direction)
            failure = not square.is_line(search_direction)

        if square.is_frame() and not self.frame_already_found(square):
            self.found_frames.append(square)
            return [square] + self.get_frames(square)
        else: return []
