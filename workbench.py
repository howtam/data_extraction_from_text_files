from IO import *
from extracter import *
from sample_profile import *

class Workbench:
    
    def __init__(self, inputSrc, outputDst, regExConfig, flowChart, outputLevels):
        self.inputSrc = inputSrc
        self.outputDst = outputDst
        self.regExConfig = regExConfig
        self.flowChart = flowChart
        self.outputLevels = outputLevels
        self.outputLevelNow = -1
        self.lastState = '__start__'
        self.lastLevel = 0
        self.lastLineNum = 0   # Use this as part of output if needed
        self.outputItems = []
        self.lineNum = 0       # Internal use only not for output
        self.regExCompile = {}

        self.extractAttrs = {}
        for key, info in regExConfig.items():
            if 'usage' in info.keys():
                id = info['usage']['id']
                lvl = id // 100
                fieldNames = info['usage']['parser'].fieldNames
                if lvl not in self.extractAttrs.keys():
                    self.extractAttrs[lvl] = {}
                self.extractAttrs[lvl][id] = dict(zip(fieldNames, [None]*len(fieldNames)))

        # print(str(self.extractAttrs))
        
        self.extract = Extract(self.extractAttrs)

        for key, value in self.regExConfig.items():
            self.regExCompile[key] = [re.compile(x) for x in value['rules']]
        # print(f" self.outputLevel {self.outputLevel}")
        
    def run(self):
        if not self.inputSrc.open(): return 'failed to open input source'
        if not self.outputDst.open(): return 'failed to open output destination'

        line, match, msg = self.findUsefulEntry()
        while msg is None:
            # print(f"----{line}")
            if match in self.flowChart[self.lastState]:
                # print(f" {match} in {self.flowChart[self.lastState]}")   
                thisLevel = self.regExConfig[match]['usage']['id'] // 100
                # print(f"id  {self.regExConfig[match]['usage']['id']}")
                if thisLevel in self.outputLevels:
                    # print(f"In print group")
                    if (self.outputLevelNow > -1 and thisLevel != self.outputLevelNow) or match in self.outputItems:
                        # print(f"{(self.outputLevelNow > -1 and thisLevel != self.outputLevelNow)} or {match in self.outputItems}")
                        self.outputDst.put(self.extract.extracted, self.inputSrc.path, self.lastLineNum)
                        self.outputItems = []
                        self.extract.resetExtract(level=min(self.outputLevels))
                    self.outputLevelNow = thisLevel
                    self.outputItems += [match]
                elif thisLevel < self.lastLevel:
                    # print('level coming down')
                    if self.lastLevel in self.outputLevels: 
                        self.outputDst.put(self.extract.extracted, self.inputSrc.path, self.lastLineNum)
                        self.outputItems = []

                    self.extract.resetExtract(level=thisLevel)
                            
                (keys, values) = self.regExConfig[match]['usage']['parser'].run(line)
                self.extract.storeExtracted(keys, values)
                self.lastState = match
                self.lastLevel = thisLevel
                self.lastLineNum = self.lineNum
            else:  # not following flowchart
                return f"line {self.lineNum} is {match} which does not follow {self.lastState}"
                    
            line, match, msg = self.findUsefulEntry() 

        if '__end__' in self.flowChart[self.lastState]:
            if self.lastLevel in self.outputLevels: self.outputDst.put(self.extract.extracted, self.inputSrc.path, self.lastLineNum)
            msg = 'input properly finished in end state'
        else:
            msg = 'input not complete'
        self.inputSrc.close()
        self.outputDst.close()
        return msg

    def findAllMatches(self, line):
        ret = list(self.regExCompile.keys())
        for key, value in self.regExCompile.items():
            for rule in value:
                if rule.match(line) is None:
                    ret.remove(key)
                    continue
        return ret
        
    def findUsefulEntry(self):
        line = self.advanceOneLine()
        while line is not None:
            matches = self.findAllMatches(line)
            if len(matches) != 1:
                return line, matches, f"line: \"{line}\" at {self.lineNum} has multiple matches {matches}"
            elif 'usage' in self.regExConfig[matches[0]].keys():
                return line, matches[0], None
            line = self.advanceOneLine()
        return None, None, "end of file reached"
        
    def advanceOneLine(self):
        line = self.inputSrc.getOneLine()

        # print(f"<<<advanceOneLine {line}>>>")
        if line is not None:
            self.lineNum += 1
        return line