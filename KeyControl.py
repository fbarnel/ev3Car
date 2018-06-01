from tty import *
from sys import *

import termios
import collections

KeyCmd=collections.namedtuple('KeyCmd',['index','key','description','handler'])

class KeyController:
    def __init__ (self, path="config.txt"):
        self.__config=[]
        self.__parse(path)
        self.__path=path

    def __parse(self, path):
        with open(path,'r') as fConfig:
            for line in fConfig:
                listParam=line.split("|")
                self.__config.append(KeyCmd(int(listParam[0]),*listParam[1:],getattr(self,"_KeyController__Handler_"+listParam[0])))

    def __len__(self):
        return len(self.__config)

    def __getitem__(self, position):
        return self.__config[position]

    def __repr__(self):
        return 'KeyController("{}")'.format(self.__path)

    def __str__(self):
        result=""
        keyCmdFmt='{0:2d} | {1:s} | {2:s}'
        for keyCmd in self.__config:
            result+=keyCmdFmt.format(*(keyCmd[i] for i in range(len(keyCmd))))
        return result

    def __contains__(self, ch=''):
        return (len([keyCmd for keyCmd in self.__config if keyCmd.key==ch])>0)

    def index(self, ch=''):
        if ch in self:
            return [keyCmd.index for keyCmd in self.__config if keyCmd.key==ch][0]
        else :
            return -1

    def __Handler_0(self):
        print("Handler0")

    def __Handler_1(self):
        print("Handler1")

    def __Handler_23(self):
        print("Handler23")

    def threadCode(self):
        defaultAttr = termios.tcgetattr(stdin.fileno())
        ch='x'
        while ch!='q':
            setraw(stdin.fileno())
            ch = stdin.read(1)
            termios.tcsetattr(stdin.fileno(), termios.TCSANOW, defaultAttr)
            if ch in self:
                self[self.index(ch)].handler()


