import subprocess
import time

class CopyClip():
    def __init__(self, sleep):
        self.sleep = sleep

    def copy2clip(self,key,tip ,value):
        print (key,'  :  ', " | %s copied to clipboard "%tip)
        (subprocess.Popen(['xsel', '-pi'], stdin = subprocess.PIPE)
                         .communicate(value.encode()))
        (subprocess.Popen(['xsel', '-bi'], stdin = subprocess.PIPE)
                         .communicate(value.encode()))
        time.sleep(self.sleep)
        tmp1 = subprocess.Popen(['xsel', '-pc'])
        tmp1.wait()
        tmp1 = subprocess.Popen(['xsel', '-bc'])
        tmp1.wait()


