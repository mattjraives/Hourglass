import curses,re

lcap = lambda x: " \\\\"+"{}"*(x-2)+"//"
ucap = lambda x: " //"+"{}"*(x-2)+"\\\\"
upper = lambda x,y: " "*y+"\\\\"+"{}"*x+"//"
lower = lambda x,y: " "*y+"//"+"{}"*x+"\\\\"
center = lambda y: " "*y+"||{}||"

N=25
K=sum([i for i in range(N+1) if i<(N+1)/2])
j = 0
glass = []
for i in range(1,N+1):
    if i<(N+1)/2.:
        nums = list(range(int((N-2*i+1)/2)))[::-1]
        if len(nums)>1:
            nums = nums + nums[:-1][::-1]
        glass.append(upper(N-2*i,i).format(*["{"+str(k)+"}" for k in nums]))
        j = max(list(range(j,j+int((N-2*i+1)/2)))[::-1])+1
    elif i>(N+1)/2.:
        nums = list(range(int((2*i-N-1)/2)))[::-1]
        if len(nums)>1:
            nums = nums + nums[:-1][::-1]
        glass.append(lower(2*i-N-2,1+N-i).format(*["{"+str(k)+"}" for k in nums]))
        j = max(list(range(j,j+int((2*i-N-1)/2)))[::-1])+1
    else:
        glass.append(center(i-1).format("{0}"))
        j = j+1
J = j
fill = ["*"]*K+[" "]*(J-K)
myscr = curses.initscr()
myscr.border(0)
myscr.addstr(1,1,ucap(N).format(*["=" for i in range(N-2)]))
myscr.addstr(2+N,1,lcap(N).format(*["=" for i in range(N-2)]))
myscr.addstr(N+4,1,"{},{},{},{}".format(N,K,J,len(fill)))
j = 0
#myscr.addstr(2,1,"\n".join(glass))
for i,pane in enumerate(glass):
#    myscr.addstr(2+i,1,pane)
    k = int((1+len(re.findall("\{",pane)))/2)
#    myscr.addstr(2+i,4*N,str(k)+"|"+str(fill[j:j+k]))
    myscr.addstr(2+i,1,pane.format(*fill[j:j+k]))
    j += k
myscr.refresh()
myscr.getch()

curses.endwin()
