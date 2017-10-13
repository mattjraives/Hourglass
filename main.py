import argparse,sys
from screen import Screen
from hourglass import Hourglass

parser = argparse.ArgumentParser(description="timer setup options")
parser.add_argument("time",type=float,help="Timer length")
parser.add_argument("--size","-s",type=int,default=25,help="Size of the hourglass")
parser.add_argument("--max",action="store_true",help="set hourglass size to maximum")

if __name__=="__main__":
    args = parser.parse_args()
    try:
        screen = Screen()
        screen.add_window(*screen.scr.getmaxyx(),0,0,"border")
        screen.windows["border"].border(0)
        screen.windows["border"].refresh()
        if args.max:
            args.size=min(screen.scr.getmaxyx())-5
        screen.add_window(args.size+5,args.size+4,1,1,"hourglass")
        glass = Hourglass(args.time,size=args.size)
        glass.start(screen.windows["hourglass"])
        glass.stop(screen.windows["hourglass"])
        screen.exit()    
    except:
        screen.exit()
        print("Unecpexted error:")
        print(sys.exc_info()[0])
        print("Exiting...")
        raise
