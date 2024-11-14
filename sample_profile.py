from extracter import *

"""
Two types of lines: one carries data and one doesn't.
Most important element is 'rules', whose value is a list of regular expressions to describe the line.

The one that does not carry data has only 'rules'.

For the other type there is addictional dict:

'usage': {  'id': 101,
            'parser': TokenExtracter(['acctNum'], [1]),} }

'id': every type of line has unique id integer number from 100 and on.
'parser' carries a object that is configured to extract the data from this line type

The digits from hundred and up designate a level.  For example, 101 mean it belongs to level 1.
The highest level number in this structure is always for output.  In our case, trans_1 and trans_2.  
Workbench object realizes the highest level and output data when needed.  Right now the rule for triggering out is that when, in this case,
any of the 900 level ids is seen the second time, the output will be done before processing the new line.
Why the concept of level?
For example there is account, subaccount, transaction types and transaction detail.  It is high level.  The text is organized like this:

account
    subaccount
        transaction type
            transaction detail
            transaction detail  <--- A
            transaction detail  <--- B
        transaction type
            transaction detail  <--- C
    subaccount
        transaction type
            transaction detail  <--- D
account  <--- E
        transaction type
            transaction detail

There could be and is often the case that account information involves more than one line of text, as shown in the example below.  
That's why the id numbers for account must be grouped together by ways of level.

......        

So there are four levels.

"""
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
    'trans_3': { 'rules': [r'^TRANS3: '], 
              'usage': {'id': 802, 
                        'parser': RegExExtracter(['stock_1', 'bye_sell_1',  'amount_1',  'amount_2'], r'TRANS3: ([A-Za-z]+)\s+(BUY|SELL)\s+(\d+)\s+(\d+)\s*$'),} },

}

"""
In this example there are two groups of transaction information.  800 and 900  
"""
outputLevels = [8, 9]

"""
for the sample structure about the flowchart is like this:
flowChart = {
    '__start__': ['account'],
    'account': ['subaccount', 'transaction type'],   # notice E
    'subaccount': ['transaction type'],
    'transaction type': ['transaction detail'],
    'transaction detail' ; ['transaction detail', 'transaction type', 'subaccount', '__end__'],    # notice A, B and C  
                                                                                                #'__end__' is where a structure is completed
                                                                                                
It must have the '__start__' key to indicate what types of first relevant line should be read
'__end__' shows the completion of the structure and also where the input should end otherwise there could be some data problem.

"""

"""
In this flowchart, there are two types of transaction information.  One is described with trans_1 and one with ( trans_1, trans_2 )
From trans_1 if the next stop is acct_1, which means it is a complete transaction description.  Of course the next stop can be trans_1 or trans_3
but that would be a new one.  if the next one is trans_2, there is more data for this transaction.

 trans_1, trans_2 and trans_3 can lead to __end__
"""

flowChart = {
    '__start__': ['acct_1'],
    'acct_1': ['acct_2'],
    'acct_2': ['trans_1'],
    'trans_1': ['trans_1', 'trans_2', 'trans_3', 'acct_1', '__end__'],
    'trans_2': ['trans_1', 'trans_3', 'acct_1', '__end__'],
    'trans_3': ['trans_1', 'trans_3', 'acct_1', '__end__']
}
