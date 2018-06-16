from tty import *
from sys import *

import termios
import collections

def add_Handler(myClass, index):
    def internalHandler(self):
        print("Handler_%d has not been set!" %index)

    internalHandler.__name__ = "_KeyController__Handler_" + str(index)
    setattr(myClass, internalHandler.__name__, internalHandler)

KeyCmd=collections.namedtuple('KeyCmd',['index','key','description','handler'])

class KeyController():
    def __init__ (self, path="config.txt"):
        self.__config=[]
        self.__parse(path)
        self.__path=path

    def __parse(self, path, firstTime=1):
        with open(path,'r') as fConfig:
            for line in fConfig:
                listParam=line.split("|")
                add_Handler(KeyController, int(listParam[0]))
                self.__config.append(KeyCmd(int(listParam[0]),listParam[1],listParam[2],getattr(self,"_KeyController__Handler_"+listParam[0]))._asdict())

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
            result+=keyCmdFmt.format(*(keyCmd[i] for i in keyCmd.keys()))
        return result

    def __contains__(self, ch=''):
        return (len([keyCmd for keyCmd in self.__config if keyCmd['key']==ch])>0)

    def __containsH__(self, handler):
        return (len([keyCmd for keyCmd in self.__config if keyCmd['handler'].__name__==("_KeyController__"+handler.__name__)])>0)

    def index(self, ch=''):
        if ch in self:
            return [keyCmd['index'] for keyCmd in self.__config if keyCmd['key']==ch][0]
        else :
            return -1

    def indexH(self, handler):
        if self.__containsH__(handler):
            return [keyCmd['index'] for keyCmd in self.__config if keyCmd['handler'].__name__==("_KeyController__"+handler.__name__)][0]
        else :
            return -1

    def handler(self, func):
        if self.__containsH__(func):
            self.__config[self.indexH(func)]['handler'] = func
        else:
            print("%s does not exist!" % func.__name__);
        return func


    def threadCode(self):
        defaultAttr = termios.tcgetattr(stdin.fileno())
        ch='x'
        while ch!='q':
            setraw(stdin.fileno())
            ch = stdin.read(1)
            termios.tcsetattr(stdin.fileno(), termios.TCSANOW, defaultAttr)
            if ch in self:
               self[self.index(ch)]['handler']()


