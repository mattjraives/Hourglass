import curses,re,sys,time,argparse

class Hourglass:
    def __init__(self,timer,size=25,grain="*"):
        self.timer = timer
        self.N = size
        self.grain = grain
        self.methods()
        self.build_glass()
    #
    def build_glass(self):
        j = 0
        glass = []
        glass.append(self.ucap(self.N).format(*["=" for i in range(self.N-2)]))
        for i in range(1,self.N+1):
            if i<(self.N+1)/2.:
                nums = list(range(int((self.N-2*i+1)/2)))
                if len(nums)>1:
                    nums = nums + nums[:-1][::-1]
                glass.append(self.upper(self.N-2*i,i).format(*["{"+str(k)+"}"\
                                                               for k in nums]))
                j = max(list(range(j,j+int((self.N-2*i+1)/2)))[::-1])+1
            elif i>(self.N+1)/2.:
                nums = list(range(int((2*i-self.N-1)/2)))
                if len(nums)>1:
                    nums = nums + nums[:-1][::-1]
                glass.append(self.lower(2*i-self.N-2,1+self.N-i).format(*["{"+str(k)+"}"\
                                                                          for k in nums]))
                j = max(list(range(j,j+int((2*i-self.N-1)/2)))[::-1])+1
            else:
                glass.append(self.center(i-1).format("{0}"))
                j = j+1
        glass.append(self.lcap(self.N).format(*["=" for i in range(self.N-2)]))
        self.J = j
        self.K=sum([i for i in range(self.N+1) if i<(self.N+1)/2])
        self.glass = glass
        self.fill = [self.grain]*self.K+[" "]*(self.J-self.K)
    #
    def start(self,window):
        self.sleep = self.timer/float(self.K)
        t0 = time.time()
        i = 0
        for i in range(self.K):
            time.sleep(self.sleep)
            self.tick(i)
            self.display(window)
            i += 1
    #
    def stop(self,window):
        window.getch()
    #
    def tick(self,i):
        self.fill[i] = " "
        self.fill[-(i+1)] = self.grain
    #
    def display(self,window):
        j = 0
        for i,pane in enumerate(self.glass):
            k = int((1+len(re.findall("\{",pane)))/2)
            f = self.fill[j:j+k]
            window.addstr(i,0,pane.format(*f))
            j += k
        window.refresh()
    #
    def methods(self):
        self.lcap = lambda x: " \\\\"+"{}"*(x-2)+"//"
        self.ucap = lambda x: " //"+"{}"*(x-2)+"\\\\"
        self.upper = lambda x,y: " "*y+"\\\\"+"{}"*x+"//"
        self.lower = lambda x,y: " "*y+"//"+"{}"*x+"\\\\"
        self.center = lambda y: " "*y+"||{}||"

if __name__=="__main__":
    args = parser.parse_args()
    if args.max:
        args.size=999999
    hg = Hourglass(args.time,size=args.size,debug=args.debug)
    #hg.scr.refresh()
    #hg.scr.getch()
    #curses.endwin()
    #print(hg.fill)
