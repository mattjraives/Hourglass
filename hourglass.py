import curses,re,sys,time,argparse

parser = argparse.ArgumentParser(description="timer setup options")
parser.add_argument("time",type=float,help="Timer length")
parser.add_argument("--size","-s",type=int,default=25,help="Size of the hourglass")
parser.add_argument("--debug",action="store_true",help="Debug Mode")

class Hourglass:
    def __init__(self,timer,size=25,grain="*",debug=0):
        self.timer = timer
        self.N = size
        self.grain = grain
        self.debug = debug
        self.methods()
        self.setup_display()
        self.build_glass()
        self.start()
    #
    def build_glass(self):
        N = self.N
        j = 0
        glass = []
        for i in range(1,N+1):
            if i<(N+1)/2.:
                nums = list(range(int((N-2*i+1)/2)))
                if len(nums)>1:
                    nums = nums + nums[:-1][::-1]
                glass.append(self.upper(N-2*i,i).format(*["{"+str(k)+"}" for k in nums]))
                j = max(list(range(j,j+int((N-2*i+1)/2)))[::-1])+1
            elif i>(N+1)/2.:
                nums = list(range(int((2*i-N-1)/2)))
                if len(nums)>1:
                    nums = nums + nums[:-1][::-1]
                glass.append(self.lower(2*i-N-2,1+N-i).format(*["{"+str(k)+"}"\
                                                                for k in nums]))
                j = max(list(range(j,j+int((2*i-N-1)/2)))[::-1])+1
            else:
                glass.append(self.center(i-1).format("{0}"))
                j = j+1
        self.J = j
        self.K=sum([i for i in range(N+1) if i<(N+1)/2])
        self.glass = glass
        self.fill = [self.grain]*self.K+[" "]*(self.J-self.K)
    #
    def setup_display(self):
        self.scr = curses.initscr()
        maxy = self.scr.getmaxyx()[0] - 4
        if not maxy%2:
            maxy = maxy-1
        if self.debug:
            maxy = maxy-2
        self.N = min([maxy,self.N])
        self.scr.border(0)
        self.scr.addstr(1,1,self.ucap(self.N).format(*["=" for i in range(self.N-2)]))
        self.scr.addstr(2+self.N,1,self.lcap(self.N).format(*["=" for i in range(self.N-2)]))
    #
    def start(self):
        self.sleep = self.timer/float(self.K)
        t0 = time.time()
        i = 0
        if self.debug:
            self.scr.addstr(self.N+4,1,"{},{},{},{},{},{}".format(self.N,self.K,self.J,\
                                                                  len(self.fill),\
                                                                  *self.scr.getmaxyx()))
        for i in range(self.K):
            time.sleep(self.sleep)
            self.tick(i)
            self.display()
            i += 1
        self.scr.getch()
        curses.endwin()
    #
    def tick(self,i):
        self.fill[i] = " "
        self.fill[-(i+1)] = self.grain
        #self.fill = [" "] + self.fill[1:]
        #self.fill[-1]
    #
    def display(self):
        j = 0
        for i,pane in enumerate(self.glass):
            k = int((1+len(re.findall("\{",pane)))/2)
            f = self.fill[j:j+k]
            self.scr.addstr(2+i,1,pane.format(*f))
            j += k
        self.scr.refresh()
    #
    def methods(self):
        self.lcap = lambda x: " \\\\"+"{}"*(x-2)+"//"
        self.ucap = lambda x: " //"+"{}"*(x-2)+"\\\\"
        self.upper = lambda x,y: " "*y+"\\\\"+"{}"*x+"//"
        self.lower = lambda x,y: " "*y+"//"+"{}"*x+"\\\\"
        self.center = lambda y: " "*y+"||{}||"

if __name__=="__main__":
    args = parser.parse_args()
    hg = Hourglass(args.time,size=args.size,debug=args.debug)
    #hg.scr.refresh()
    #hg.scr.getch()
    #curses.endwin()
    #print(hg.fill)
