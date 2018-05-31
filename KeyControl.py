import collections

KeyCmd=collections.namedtuple('KeyCmd',['index','key','description'])

class KeyController:
    def __init__ (self, path="config.txt"):
        self.__config=[]
        self.__parse(path)
        self.__path=path

    def __parse(self, path):
        with open(path,'r') as fConfig:
            for line in fConfig:
                listParam=line.split("|")
                self.__config.append(KeyCmd(int(listParam[0]),*listParam[1:]))

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
