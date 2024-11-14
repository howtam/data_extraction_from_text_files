import re

class LineParser:
    def __init__(self, regex, fieldNames):
        self.regex = regex
        self.fieldNames = fieldNames
        self.numFields = len(self.fieldNames)
        self.re = re.compile(self.regex)
        
    def run(self, line):
        m = self.re.findall(line)
        return self.fieldNames, [m[0]] if self.numFields == 1 else list(m[0])

    def getFieldNames(self):
        return self.fieldNames
    
regExConfig = {
    '__blank__': { 'rules': [r'^\s*$'], },
    '__dash__': { 'rules': [r'^-+'], },
    'acct_1': { 'rules': [r'^ACCT: [\d]+'], 
               'usage': {'id': 101, 
                        'parser': LineParser(r'ACCT: (\d+)', ['acctNum']),} },
    'acct_2': { 'rules': [r'^NAME: [^\s]+'], 
               'usage': {'id': 102, 
                        'parser': LineParser(r'NAME: ([A-Za-z]+)\s*$', ['name']),} },
    'trans_1': { 'rules': [r'^TRANS1: '], 
              'usage': {'id': 901, 
                        'parser': LineParser( r'TRANS1: ([A-Za-z]+)\s+(BUY|SELL)\s+(\d+)\s*$', ['stock_1', 'bye_sell_1',  'amount_1']),} },
    'trans_2': { 'rules': [r'^TRANS2: '], 
              'usage': {'id': 902, 
                        'parser': LineParser( r'TRANS2: ([A-Za-z]+)\s+(BUY|SELL)\s+(\d+)\s*$', ['stock_2', 'bye_sell_2',  'amount_2']),} },
    }

flowChart = {
    '__start__': ['acct_1'],
    'acct_1': ['acct_2'],
    'acct_2': ['trans_1'],
    'trans_1': ['trans_1', 'trans_2', 'acct_1', '__end__'],
    'trans_2': ['trans_1', 'acct_1', '__end__']
}
