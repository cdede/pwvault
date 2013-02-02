
from Crypto.Protocol.KDF import PBKDF2
from base64 import b64encode,b64decode
import os

class Cpassnum(object):
    def __init__(self, salt,iter0 = 5000,saltlen=36):
        self.salt=salt
        self.iter0=iter0
        self.saltlen=saltlen

    def getkey(self,num):
        iterations = self.iter0+num
        key = PBKDF2(str(num), self.salt, dkLen=32, count=iterations)
        key = b64encode(key).decode()
        return key

    def gen_salt(self):
        salt = os.urandom(self.saltlen)
        return b64encode(salt)



