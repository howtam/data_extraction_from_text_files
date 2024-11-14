from extracter import *

regExConfig = {
    '__blank__': { 'rules': [r'^\s*$'], },
    '__dash__': { 'rules': [r'^-+\s*$'], },
    'acct_1': { 'rules': [r'^ACCT: [\d]+'], 
               'usage': {'id': 101, 
                        'parser': TokenExtracter(['acctNum'], [1]),} },
    'acct_2': { 'rules': [r'^NAME: [^\s]+'], 
               'usage': {'id': 102, 
                        'parser': RegExExtracter(['name'], r'NAME: ([A-Za-z]+)\s*$'),} },
    'trans_1': { 'rules': [r'^TRANS1: '], 
              'usage': {'id': 901, 
                        'parser': TokenExtracter(['stock_1', 'bye_sell_1',  'amount_1'], [1,2,3]),} },
    'trans_2': { 'rules': [r'^TRANS2: '], 
              'usage': {'id': 902, 
                        'parser': RegExExtracter(['stock_2', 'bye_sell_2',  'amount_2'], r'TRANS2: ([A-Za-z]+)\s+(BUY|SELL)\s+(\d+)\s*$'),} },
    }

flowChart = {
    '__start__': ['acct_1'],
    'acct_1': ['acct_2'],
    'acct_2': ['trans_1'],
    'trans_1': ['trans_1', 'trans_2', 'acct_1', '__end__'],
    'trans_2': ['trans_1', 'acct_1', '__end__']
}