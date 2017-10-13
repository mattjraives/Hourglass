import curses

class Screen():
    def __init__(self):
        self.scr = curses.initscr()
        self.scr.border(0)
        self.windows = {}
        self.setup()
        self.scr.refresh()
    def setup(self):
        self.scr.clear()
        curses.noecho()
        curses.cbreak()
        self.scr.keypad(True)
        curses.curs_set(False)
    def exit(self):
        self.scr.clear()
        curses.nocbreak()
        self.scr.keypad(False)
        curses.curs_set(True)
        curses.echo()
        curses.endwin()
    def add_window(self,dy,dx,y,x,label=None):
        if not label:
            label = "Window {}".format(len(self.windows))
        self.windows[label] = curses.newwin(dy,dx,y,x)
    
