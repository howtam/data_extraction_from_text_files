import pandas as pd
import copy
class Extract():
    def __init__(self, extractAttrs):
        self.extractAttrs = extractAttrs
        self.extracted = {}
        for level, group in extractAttrs.items():
            for id, value in group.items():
                self.extracted |= value
     
    def resetExtract(self, level=1):
        for lvl, group in self.extractAttrs.items():
            if lvl >= level:
                for id, attrs in group.items():
                    for attr, value in attrs.items():
                        self.extracted[attr] = value  

    def getExtracted(self, keys):
        ret = {}
        for key in keys:
            try:
                ret |= { key: self.extracted[key] }
            except:
                pass
        return ret

    def getAllExtracted(self):
        return copy.copy(self.extracted)

    def storeExtracted(self, keys, values):
        for i in range(len(keys)):
            self.extracted[keys[i]] = values[i]

class TextInput:
    def __init__(self, path):
        self.path = path
        self.file = None

    def open(self):
        try:
            self.file = open(self.path, 'r')
            return True
        except:
            return False

    def fileOpened(self):
        return self.file != None

    def close(self):
        if self.file: 
            self.file.close()
            self.file = None

    def getOneLine(self):
        if self.file is None: 
            return None
        try:
            l = self.file.readline()
            # print ( f"[[[ getOneLine {l}]]]")
            if l == '': return None
            return l.replace('\n', '')
        except:
            return None

    def __del__(self):
        if self.file: 
            self.file.close()

class OutputBase:
    def open(self):
        return True

    def close(self):
        pass

    def put(self, extractDict):
        return True

class CsvOutput(OutputBase):
    def __init__(self, path):
        self.path = path
        self.count = 0
        self.df = None

    def open(self):
        return True
        
    def close(self):
        self.df.to_csv(self.path, sep=',', index=False)

    def put(self, extractDict):
        if self.df is None:
            self.df = pd.DataFrame(columns=list(extractDict.keys()), dtype=str) 
        self.df.loc[len(self.df)]=(list(extractDict.values()))
        self.count+=1

      
class StdOutput(OutputBase):
    def put(self, extractDict):
        print(extractDict)
        return True

class DictOutput(OutputBase):
    def __init__(self, path, dictName):
        self.path = path
        self.dictName = dictName

    def open(self):
        try:
            self.file = open(self.path, 'w')
            self.file.write(self.dictName+' = [\n')
            return True
        except Exception  as  e:
            print (e)
            return False

    def close(self):
        self.file.write(']\n')
        self.file.close()

    def put(self, extractDict):
        try:
            self.file.write(str(extractDict)+',\n')
            return True
        except Exception  as  e:
            print (e)
            return False
