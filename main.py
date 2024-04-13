import subprocess
import os
import io
import sys
import keyboard
def cmd_exit(c,p):
    exit()
def cmd_cd(c,p):
    try:
        os.chdir(os.path.abspath(p[1]))
    except Exception:
        print("Path not found: {}".format(p[1]))
def do_nothing(c,p):
    print("")
cmd = {
    "exit": cmd_exit,
    "cd": cmd_cd,
    "#": do_nothing
}

def run_prog(c):
    try:
        if "|" in c:
            s_in , s_out = (0,0)
            #Make copy of standard in/out
            s_in = os.dup(0)
            s_out = os.dup(1)
            

            fdin = os.dup(s_in)

            for cmd in c.split("|"):
                os.dup2(fdin,0)
                os.close(fdin)

                if cmd == c.split("|")[-1]:
                    #print out result
                    fdout = os.dup(s_out)
                else:
                    #Copy fdout to fdin
                    fdin, fdout = os.pipe()

                os.dup2(fdout,1)
                os.close(fdout)
                try:
                    subprocess.run(cmd.strip().split())
                except Exception:
                    print("Cant run {}".format(c))
            os.dup2(s_in,0)
            os.dup2(s_out,1)
            os.close(s_in)
            os.close(s_out)
        else:
            
            subprocess.run(c.split())
    except Exception:
        print("Cant pipe {}".format(c))
        
def cmd_line(r):
    if r.split()[0] != "^":
        try:
            cmd[r.split(" ")[0]](r, r.split(" "))
        except Exception:
            run_prog(r)

#keyboard.write("hello")
while True:
    r = input(f"\033[94m{os.getcwd()}\033[0m $ ")
    cmd_line(r)
    
    
    
