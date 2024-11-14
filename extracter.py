import re
class ExtracterBase:
    def __init__(self, fieldNames):
        self.fieldNames = fieldNames
        self.numFields = len(self.fieldNames)
        
    def run(self, line):
        return self.fieldNames, [None]*self.numFields
        
    def getFieldNames(self):
        return self.fieldNames
        
class RegExExtracter(ExtracterBase):
    def __init__(self, fieldNames, regex):
        super().__init__(fieldNames)
        self.regex = regex
        self.re = re.compile(self.regex)
        
    def run(self, line):
        m = self.re.findall(line)
        return self.fieldNames, [m[0]] if self.numFields == 1 else list(m[0])

class TokenExtracter(ExtracterBase):
    def __init__(self, fieldNames, tokenIdx):
        super().__init__(fieldNames)
        self.tokenIdx = tokenIdx
        
    def run(self, line):
        tokens = line.split()
        return self.fieldNames, [ tokens[i] for i in self.tokenIdx]