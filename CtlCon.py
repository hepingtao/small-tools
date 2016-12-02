#!/usr/bin/python
# -*- coding:utf-8 -*-

import xdrlib, sys
import xlrd
import datetime
import os
import re

reload(sys)
sys.setdefaultencoding("utf-8")

def ReadCfgFileCfgInfo(CfgFile):
    BaseCfgFileName = os.path.splitext(os.path.basename(CfgFile))[0]
    CfgFileDict    = {}
    CfgFileCfgDict = {}
    tmpCfgFileCfgDict = {}
    Key   = ""
    Value = ""
    f = OpenFile(CfgFile)
    lineID = 0
    for line in f:
        lineID = lineID + 1

        searchVerObj = re.search(r'^(version)=(.*)$', line, re.I|re.M)
        searchKeyObj = re.search(r'^\[(insert_update_job|del_job|insert_update_ds|del_ds)\].*$', line, re.I|re.M)
        ##TW_BUSS_SGSNPGW_USR_MON($YYYY)($MM)_($SSSSSS)_($S).gz
        #searchValueObj = re.search(r'^[A-Za-z0-9_\.,\(\)\$ ]+.*$', line, re.I|re.M)
        searchValueObj = re.search(r'^[^#\s].*$', line, re.I|re.M)
        if searchVerObj:
            Key   = searchVerObj.group(1)
            print Key
            Value = searchVerObj.group(2)
            [ReqID, ReqName] = re.split(r',| +', Value)
            if BaseCfgFileName != ReqID:
                print "The version ID of Cfg info is wrong, not as same as cfg filename, please modify it first!"
                sys.exit(1)
            #CfgFileCfgDict[Key] = ReqID
            CfgFileCfgDict[Key] = [ReqID, ReqName]
            tmpCfgFileCfgDict = {}
            tmpCfgFileCfgDict[Key] = [ReqID, ReqName]
            CfgFileDict[lineID] = tmpCfgFileCfgDict
            #Key = ""
        elif searchKeyObj:
            Key = searchKeyObj.group(1)
            print Key
            CfgFileCfgDict[Key] = []
            tmpCfgFileCfgDict = {}
            tmpCfgFileCfgDict[Key] = []
            CfgFileDict[lineID] = tmpCfgFileCfgDict
        elif searchValueObj:
            ValueList = re.split(',| +', line)
            print ValueList
            CfgFileCfgDict[Key].append(ValueList)
            tmpCfgFileCfgDict[Key].append(ValueList)
            #print tmpCfgFileCfgDict
        else:
            CfgFileDict[lineID] = [line]
            #continue
    #print CfgFileCfgDict
    #sys.exit(1)

    return CfgFileDict, CfgFileCfgDict
    
    
def GetLatestCodeID(LatestCodeIDFile, CodeIDDict, MaxDsID):
    CodeType = ""
    CodeID   = ""
    LatestCodeIDDict = {}

    f = OpenFile(LatestCodeIDFile)
    for line in f:
        #print line
        ValueList = re.split(':|,| +', line)
        CodeType  = ValueList[0]
        CodeID    = int(ValueList[1])

        TmpValue  = 0
        try:
            TmpValue = CodeIDDict[CodeID]
        except:
            pass

        while TmpValue == 1:
            CodeID = CodeID + 1
            try:
                TmpValue = CodeIDDict[CodeID]
            except:
                TmpValue = 0

        LatestCodeIDDict[CodeType] = CodeID

    #DsID = MaxDsID + 1
    #LatestCodeIDDict['DS'] = DsID

    print LatestCodeIDDict
    #sys.exit(1)

    return LatestCodeIDDict


def ReadCfgFile(CfgFile):
    CfgFileDict = {
                   'insert_update_job': '',
                   'del_job'          : '',
                   'insert_update_ds' : '',
                   'del_ds'           : ''
                  }
    Key   = ""
    Value = ""
    f = OpenFile(CfgFile)
    for line in f:
        searchObj = re.search(r'^(version)=(.*)$', line, re.I|re.M)
        if searchObj:
            Key   = searchObj.group(1)
            Value = searchObj.group(2)
            CfgFileDict[Key] = Value
            #Key = ""

        searchKeyObj = re.search(r'^\[(insert_update_job|del_job|insert_update_ds|del_ds)\].*$', line, re.I|re.M)
        searchValueObj = re.search(r'^\d[0-9, ]+ *$', line, re.I|re.M)
        #searchValueObj = re.search(r'^\d[A-Za-z0-9_\., ]* *$', line, re.I|re.M)
        if searchKeyObj:
            Key = searchKeyObj.group(1)
            CfgFileDict[Key] = []
        elif searchValueObj:
            ValueList = re.split(',| ', line)
            #print TmpValueList
            for Value in ValueList:
                #print v
                Value = Value.strip()
                CfgFileDict[Key].append(Value)
        else:
            continue

    #print CfgFileDict
    return CfgFileDict
    
    
def OpenExcel(ExcelFile):
    #data = xlrd.open_workbook(ExcelFile)
    #return data
    print ExcelFile
    #xlrd.Book.encoding = "utf-8"
    try:
        #data = xlrd.open_workbook(ExcelFile, encoding_override = "gb2312")
        #data = xlrd.open_workbook(ExcelFile, on_demand = True, encoding_override = "utf_16_le", formatting_info=True)
        #data = xlrd.open_workbook(ExcelFile, on_demand = True, encoding_override = "gb2312")
        data = xlrd.open_workbook(ExcelFile, on_demand = True)
        #sys.exit(1)
        #data = xlrd.open_workbook(ExcelFile)
        #print data
        #if data.nsheets <= 0:
        #    return Exception
        return data
    except Exception,e:
        print str(e)
        #pass


def OpenFile(FileName):
    try:
        f = open(FileName,'r')
        return f
    except Exception,e:
        print str(e)


def GetCodeConfDict(Sheet, IDCodeDict, CodeNameDict):
    nrows = Sheet.nrows  #rows
    ncols = Sheet.ncols  #cols
    #print LatestCodeIDDict
    #print IDCodeDict
    #sys.exit(1)
    CodeConfDict = {}
    #CodeNameDict = {}
    CodeName = ""
    DsCfgFlag = ""
    RePat = '数据源'
    RePat = RePat.decode('gbk')

    for IDType in IDCodeDict:
        searchDsObj  = re.search(r'_ds$',  IDType, re.I|re.M)
        searchJobObj = re.search(r'_job$', IDType, re.I|re.M)
        IDCodeList = IDCodeDict[IDType]
        #sys.exit(1)
        CodeNameList = CodeNameDict.keys()
        print CodeNameList
        #sys.exit(1)
        #print CodeNameDict
        #sys.exit(1)
        Col2Value = Sheet.row_values(0)[1]
        #print Col2Value
        #sys.exit(1)
        searchDsCfgObj = re.search(RePat, Col2Value, re.I|re.M)
        if searchDsCfgObj:
            DsCfgFlag = '1'
        #print DsCfgFlag
        if (searchDsObj and DsCfgFlag == "") or (searchJobObj and DsCfgFlag):
            continue

        for rownum in range(0, nrows):
            rowvaluelist = Sheet.row_values(rownum)
            #sys.exit(1)
            if searchDsObj and DsCfgFlag:
                #print DsCfgFlag
                #CodeName = ""
                CellValue = rowvaluelist[5]
                CellValue = re.sub(r' |\n', '', CellValue)   
                #CellValue = CellValue.encode('gbk')
                #print CodeNameList
                #if CellValue == CodeName:
                #print CodeNameList
                #sys.exit(1)
                TmpValue = ""
                if CellValue in CodeNameList:
                #print CellValue
                    CodeName = CellValue
                    TmpValue = CodeNameDict[CodeName]
                #TmpValue = CodeNameDict[CodeName]
                #print TmpValue
                if TmpValue:
                    RowID = rowvaluelist[0]
                    RowID = int(RowID)
                    CodeDesc     = rowvaluelist[2]
                    #CodeDesc    = CodeDesc.encode('gbk')
                    ColCnt       = rowvaluelist[3]
                    ColCnt       = re.sub(r'\.0+$', '', str(ColCnt))
                    Delimiter    = rowvaluelist[4]
                    Delimiter    = re.sub('，'.decode('gbk'), r',', Delimiter)
                    #CodeName     = rowvaluelist[5]
                    CodeName     = CellValue
                    Utf8Flag     = rowvaluelist[6]
                    LoadTable    = rowvaluelist[7]
                    TabPartType  = rowvaluelist[8]
                    DsFilePath   = rowvaluelist[9]
                    DsFileCycle  = rowvaluelist[11]
                    DsFileCount  = rowvaluelist[12]
                    DsFileCount  = re.sub(r'\.0+$', '', str(DsFileCount))
                    DsFileHeader = rowvaluelist[13]
                    DsStartDate  = rowvaluelist[16]
                    DsEndDate    = rowvaluelist[17]
                    CityRange    = "Gmcc"
                    #print RowID, CodeDesc, CodeName
                    CodeDesc    = re.sub(r' |\n', '', CodeDesc   )   
                    CodeName    = re.sub(r' |\n', '', CodeName   )   
                    DsFileCycle = re.sub(r' |\n', '', DsFileCycle)   
                    TabPartType = re.sub(r' |\n', '', TabPartType)   
                    CodeConfDict[RowID] = [IDType, 'DsID', TmpValue, CodeDesc, ColCnt, Delimiter, CodeName, Utf8Flag, LoadTable, TabPartType, DsFilePath, DsFileCycle, DsFileCount, DsFileHeader, DsStartDate, DsEndDate, CityRange]
                else:
                    pass
                #sys.exit(1)

            elif searchJobObj and DsCfgFlag == "":
                #print DsCfgFlag
                #CodeName = ""
                rowvaluelist = Sheet.row_values(rownum)
                CellValue = rowvaluelist[3]
                CellValue = re.sub(r' |\n', '', CellValue)   
                #CellValue = CellValue.encode('gbk')
                #print CellValue
                #if CellValue == CodeName:
                TmpValue = ""
                if CellValue in CodeNameList:
                    print CellValue
                    CodeName = CellValue
                    TmpValue = CodeNameDict[CodeName]
                CodeType = ""
                if TmpValue:
                    RowID = rowvaluelist[0]
                    RowID = int(RowID)
                    CodeDesc    = rowvaluelist[2]
                    #CodeDesc    = CodeDesc.encode('gbk')
                    #CodeName    = rowvaluelist[3]
                    CodeName    = CellValue
                    CodeCycle   = rowvaluelist[8]
                    CodePreRef  = rowvaluelist[9]
                    CodeOprObj  = rowvaluelist[10]
                    CodePreRef = CodePreRef.upper()
                    CodeOprObj = CodeOprObj.upper()
                    CodeTabPart = rowvaluelist[11]
                    if re.search(r'^[0-9]\.*[0-9]*$', str(CodeTabPart), re.I|re.M):
                        CodeTabPart = str(CodeTabPart)
                    #CodeTabPart = CodeTabPart[0:2]

                    CodeDesc    = re.sub(r' |\n', '', CodeDesc   )   
                    CodeName    = re.sub(r' |\n', '', CodeName   )   
                    CodeCycle   = re.sub(r' |\n', '', CodeCycle  )   
                    CodePreRef  = re.sub(r' |\n', '', CodePreRef )   
                    CodeOprObj  = re.sub(r' |\n', '', CodeOprObj )   
                    print CodeOprObj
                    fuck = re.search(r'(（|\()([0-9]*)(\)|）)', CodeOprObj.encode('gbk'), re.I|re.M)   
                    #print fuck.group(0).decode('gbk'), fuck.group(1), fuck.group(2), fuck.group(3)
                    CodeOprObj  = re.sub(r'(（|\()([0-9]*)(\)|）)', r'(\2)', CodeOprObj.encode('gbk'))   
                    print CodeOprObj
                    #sys.exit(1)
                    CodeOprObj  = re.sub(r'([A-Z0-9])$', r'\1(0)$', CodeOprObj )   
                    CodeTabPart = re.sub(r' |\n', '', CodeTabPart)   

                    #print RowID, CodeDesc, CodeName
                    searchCodeObj = re.search(r'^PRO_([A-Z]+)_.*$', CodeName, re.I|re.M)
                    CodeType = searchCodeObj.group(1)
                    RowID = int(RowID)
                    CityRange = "Gmcc"
                    CodeConfDict[RowID] = [IDType, CodeType, TmpValue, CodeDesc, CodeName, CityRange, CodeCycle, CodeTabPart, [CodePreRef], [CodeOprObj]]
                    #CodeConfDict[RowID] = [CodeType, TmpValue, CodeDesc, CodeName, CodeCycle, CodeTabPart, [CodePreRef], [CodeOprObj]]
                    #print CodeConfDict
                elif CodeName and CellValue != "" and TmpValue == "":
                    #print CodeName
                    CodeName = ""
                elif CodeName and CellValue == "" and TmpValue == "":
                    #print CodeName
                    CodePreRef = rowvaluelist[9]
                    CodeOprObj = rowvaluelist[10]
                    CodePreRef = CodePreRef.upper()
                    CodeOprObj = CodeOprObj.upper()
                    #print CodeOprObj

                    CodeDesc    = re.sub(r' |\n', '', CodeDesc   )   
                    CodeName    = re.sub(r' |\n', '', CodeName   )   
                    CodeCycle   = re.sub(r' |\n', '', CodeCycle  )   
                    CodePreRef  = re.sub(r' |\n', '', CodePreRef )   
                    CodeOprObj  = re.sub(r' |\n', '', CodeOprObj )   
                    #print CodeOprObj
                    #CodeOprObj  = re.sub('（([0-9]*)）', r'(\1)', CodeOprObj)   
                    CodeOprObj  = re.sub(r'(（|\()([0-9]*)(\)|）)', r'(\2)', CodeOprObj.encode('gbk'))   
                    #print CodeOprObj
                    #sys.exit(1)
                    CodeOprObj  = re.sub(r'([A-Z0-9])$', r'\1(0)$', CodeOprObj)   
                    #print CodeOprObj
                    CodeTabPart = re.sub(r' |\n', '', CodeTabPart)   

                    if CodePreRef: CodeConfDict[RowID][8].append(CodePreRef)
                    if CodeOprObj: CodeConfDict[RowID][9].append(CodeOprObj)
                    #print CodeConfDict
                    #sys.exit(1)
                else:
                    pass
                    #sys.exit(1)
                #print CellValue, rowvaluelist[10]
                #print CodeName , CellValue , TmpValue
    #print CodeConfDict
    #sys.exit(1)
    for RowID in sorted(CodeConfDict):
        #print CodeConfDict[RowID], "\n"
        print RowID
        for item in CodeConfDict[RowID]:
            print item,
        print "\n"
    #print CodeConfDict

    #print LatestCodeIDDict
    #sys.exit(1)

    return CodeConfDict
           

def GetSheetInfo(CtlTableList):
    SheetDict = {}
    f = OpenFile(CtlTableList)
    SheetID = 0
    for line in f:
        #line = str(line)
        #line = line.replace('\n','')
        line = line.strip()
        TableCols = re.split(' *, *', line)
        #print line
        #SheetIDList.append(SheetID)
        SheetID = SheetID + 1
        SheetDict[SheetID] = TableCols
    #print SheetNameList
    return SheetDict

def ReadExcel(ExcelHandle, SheetName, CfgFileCfgDict, CodeNameDict):
    #print SheetName
    CodeConfDict = {}
    IDCodeDict   = {}

    print CfgFileCfgDict
    #print ExcelHandle.nsheets
    #for sid in range(ExcelHandle.nsheets):
    #    print sid
    #for sn in ExcelHandle.sheet_names():
    #    print sn
    #sheet = ExcelHandle.sheet_by_index(1)
    #sys.exit(1)

    #for IDType in CfgFileCfgDict:
    #    print IDType
    print CfgFileCfgDict['insert_update_ds']
    print CfgFileCfgDict['insert_update_job']
    IDCodeDict['insert_update_ds']  = CfgFileCfgDict['insert_update_ds']
    IDCodeDict['insert_update_job'] = CfgFileCfgDict['insert_update_job']
    print IDCodeDict
    #sys.exit(1)

    #print SheetName
    SheetNameList = re.split(' *, *| +', SheetName)
    for SheetName in SheetNameList:
        print SheetName
        #sys.exit(1)
        #SheetName = SheetName.decode('gbk')
        Sheet = ExcelHandle.sheet_by_name(SheetName)
        tmpCodeConfDict = GetCodeConfDict(Sheet, IDCodeDict, CodeNameDict)
        if tmpCodeConfDict:
            for RowID in sorted(tmpCodeConfDict):
                CodeConfDict[RowID] = tmpCodeConfDict[RowID]

    return CodeConfDict


def WriteFile(ReqID, CtlConfDict, LatestCodeIDDict, LatestCodeIDFile, OutputPath):
    lineIDDict = {}
    CTLDataDict = {}
    OutputFile = OutputPath + "/" + ReqID + ".IN"
    #DDL = DDL.encode('cp936')
    print OutputFile
    #if os.path.exists(OutputFile):
    #    os.unlink(OutputFile)
    #try:
    #    os.remove(OutputFile)
    #except OSError:
    #    pass
    f = open(OutputFile,"a")
    Del = '\t'
    for CtlSheetName in CtlConfDict:
        CtlFileName = CtlSheetName + ".txt"
        f.write(CtlFileName)
        f.write("\n")
        #f.write("\n")
        #print CtlConfDict[CtlSheetName]
        #lineID = 0
        for ValueList in CtlConfDict[CtlSheetName]:
            ValueList = [Str.decode('gbk').strip() for Str in ValueList]
            ValueStr = Del.join(ValueList)
            ValueStr = ValueStr.strip('\n')
            #ValueStr = ValueStr.decode('gbk')
            #print ValueStr
            f.write(ValueStr)
            f.write("\n")
        f.write("\n")
                    
    f.close()

    #f = open(LatestCodeIDFile, "w")
    #for CodeType in LatestCodeIDDict:
    #    ValueStr = CodeType + ":" + str(LatestCodeIDDict[CodeType])
    #    f.write(ValueStr)
    #    f.write("\n")

    #f.close()


def UpdateCtl(FullCTLFileName, lineIDDict, CTLDataDict):
    try:
        os.remove(FullCTLFileName)
    except OSError:
        pass
    f = open(FullCTLFileName, 'a')
    for lineID in sorted(lineIDDict):
        KeyStr   = lineIDDict[lineID]
        ValueStr = CTLDataDict[KeyStr]
        ValueStr = ValueStr.rstrip('\r')
        #ValueStr = ValueStr.encode('gbk')
        if ValueStr:
            f.write(ValueStr)
            f.write('\n')
    f.close()


def ReadCTLData(FullCTLFileName, KeyColList):
    CTLDataDict = {}
    lineIDDict = {}
    try:
        f = open(FullCTLFileName, 'r')
    except:
        return lineIDDict, CTLDataDict
    lineID = 0
    for line in f:
        lineID = lineID + 1
        line = line.strip()
        ValueList = line.split(',')
        KeyStr = ""
        for ColID in KeyColList:
            ColID = int(ColID) - 1
            try:
                Cell = str(ValueList[ColID])
            except:
                Cell = ""
            if KeyStr:
                KeyStr = KeyStr + Del + Cell
            else:
                KeyStr = Cell

        lineIDDict[lineID] = KeyStr
        CTLDataDict[KeyStr] = line

    f.close()
    #sys.exit(1)

    return lineIDDict, CTLDataDict

def GetTemplateDict(TemplateFile):
    TemplateDict = {}

    f = OpenFile(TemplateFile)
    LineList = []
    TemplateType = ""
    for line in f:
        #print line
        LineList = re.split(r',', line)
        TemplateType = LineList[0]
        #del LineList[0]
        #print LineList
        TmpValue = ""
        try:
            TmpValue = TemplateDict[TemplateType]
        except:
            pass
        if TmpValue == "":
            TemplateDict[TemplateType] = []
        TemplateDict[TemplateType].append(LineList[1:])

    return TemplateDict


def GetJobInfo(ExcelHandle, SheetDict):
    Job_OnlineFile = r'/home/hector/bin/CTL.JOB_ONLINE_ATTR.txt'
    MaxRunstatJobID = 0
    MaxDsID= 0
    JobCityRangeDict = {}
    JobTwiceDict = {}
    RunstatJobDict = {}
    JobOnlineAttrDict = {}
    CodeIDDict = {}

    f = OpenFile(Job_OnlineFile)
    for line in f:
        line = line.strip()
        LineList = []
        #LineList = line.split(r',')
        LineList = re.split(r',', line)
        JobID     = ""
        CityRange = ""
        try:
            JobID     = LineList[0]
            JobID     = str(int(JobID))
            CityRange = LineList[1]
            CodeCycle = LineList[2]
        except:
            pass

        JobOnlineAttrDict[JobID] = [CityRange, CodeCycle]
        #sys.exit(1)
    #print JobOnlineAttrDict
    #sys.exit(1)

    SheetNameList = ['CTL.JOB_WNMS', 'CTL.JOB_DEF', 'CTL.TA_ETL_DS_DEF', 'CTL.JOB_PARAM_DEF']
    for SheetName in SheetNameList:
        #print SheetName
        Sheet = ExcelHandle.sheet_by_name(SheetName)
        nrows = Sheet.nrows   #rows
        ncols = Sheet.ncols   #cols
        Cols  = [int(SheetDict[SheetID][1]) for SheetID in SheetDict if SheetDict[SheetID][0] == SheetName][0]
        #print nrows
        #sys.exit(1)
        for LineID in range(0, nrows):
            rowvaluelist = Sheet.row_values(LineID)
            LineList = [re.sub(r'\.0.*$', "", str(value)) for value in rowvaluelist]
            try:
                CodeID = int(LineList[0])
            except:
                CodeID = 0
            #print LineList
            #sys.exit(1)
            #OldCtlConfDict[SheetName].append(rowvaluelist[0:Cols])
            if SheetName == 'CTL.JOB_WNMS':
                JobID = LineList[0]
                #print JobID
                JobTwiceDict[JobID] = '1'

            if SheetName in ('CTL.JOB_DEF', 'CTL.TA_ETL_DS_DEF'):
                try:
                    CodeIDDict[CodeID] = 1
                except:
                    pass

                if SheetName == 'CTL.TA_ETL_DS_DEF':
                    MaxDsID = CodeID if CodeID > MaxDsID else MaxDsID

                if SheetName == 'CTL.JOB_DEF':
                    JobID     = ""
                    CityRange = ""
                    try:
                        JobID     = LineList[0]
                        CityRange = LineList[19]
                        #CityRange = CityRange.strip()
                    except:
                        pass

                    #print JobID, CityRange
                    searchCR_CmccObj = re.search(r'GMCC', CityRange, re.I|re.M)
                    if searchCR_CmccObj:
                        CityRange = 'Gmcc'
                    else:
                        CityRange = 'City'
                    #print JobID, CityRange

                    JobCityRangeDict[JobID] = CityRange

            if SheetName == 'CTL.JOB_PARAM_DEF':
                JobID       = ""
                Param_ID    = ""
                Param_name  = ""
                Param_value = ""
                try:
                    JobID       = LineList[0]
                    Param_ID    = LineList[1]
                    Param_name  = LineList[4]
                    Param_value = LineList[6]
                except:
                    pass

                TwiceFlag = '0'
                try:
                    TwiceFlag = JobTwiceDict[JobID]
                except:
                    pass
                       
                ##MaxRunstatJobID
                searchRsProgObj = re.search(r'runstats', Param_value, re.I|re.M)

                ##Runstat
                searchPID_RsObj   = re.search(r'targettab', Param_ID, re.I|re.M)
                searchPName_RsObj = re.search(r'runstat', Param_name, re.I|re.M)

                ##Prog
                searchPID_ProgObj    = re.search(r'program', Param_ID, re.I|re.M)
                searchPName_ProgObj  = re.search(r'Perl', Param_name, re.I|re.M)
                ##"$progpath+/perl/PRO_TW_SAI_SOCBASE_HR.pl"
                searchPValue_ProgObj = re.search(r'^"\$.*?(PRO_((.*?)_.*?))(\.pl)"$', Param_value, re.I|re.M)

                ##Load
                searchPID_LoadObj   = re.search(r'loadtab', Param_ID, re.I|re.M)
                searchPName_LoadObj = re.search(r'LOAD', Param_name, re.I|re.M)

                ##Param_value
                searchPValue_CycleObj = re.search(r'^".*_([A-Z]{1,})[\.pl]*"$', Param_value, re.I|re.M)

                if searchRsProgObj:
                    #print JobID
                    try:
                        JobID = int(JobID)
                    except:
                        JobID = 0
                    MaxRunstatJobID = JobID if JobID > MaxRunstatJobID else MaxRunstatJobID

                if searchPValue_CycleObj:
                    #print Param_value
                    CodeCycle = searchPValue_CycleObj.group(1)
                    CodeCycle = CodeCycle.capitalize()
                    TmpValue = ""
                    try:
                        TmpValue = JobOnlineAttrDict[JobID]
                    except:
                        pass
                    if CodeCycle in ['Day', 'Hr']:
                        CodeCycle = 'Day'
                    elif CodeCycle in ['Mon']:
                        CodeCycle = 'Mon'
                    elif TmpValue:
                        CodeCycle = TmpValue[1]
                    else:
                        CodeCycle = 'None'
                    CityRange = 'None'
                    try:
                        CityRange = JobCityRangeDict[JobID]
                    except:
                        if TmpValue: CityRange = TmpValue[0]

                RunstatOprObj_Tab = ""
                if searchPID_RsObj and searchPName_RsObj:
                    RunstatOprObj_Tab = Param_value
                    RunstatOprObj_Tab = RunstatOprObj_Tab.replace('"','')
                    RunstatOprObj_Tab = RunstatOprObj_Tab.upper()
                    RunstatJobDict[RunstatOprObj_Tab] = [JobID, CityRange, CodeCycle, TwiceFlag]
                #else:
                if searchPID_ProgObj and searchPName_ProgObj and searchPValue_ProgObj:
                    #Param_value = Param_value.replace('"','')
                    #print Param_value
                    #searchProgObj = re.search(r'^\$.*?PRO_((.*?)_.*?)\.pl\s*$', Param_value, re.I|re.M)
                    try:
                        ProgName    = searchPValue_ProgObj.group(1)
                        ProgTabName = searchPValue_ProgObj.group(2)
                        ProgSchema  = searchPValue_ProgObj.group(3)
                        ProgSuffix  = searchPValue_ProgObj.group(4)
                        TabSchema   = ProgSchemaDict[ProgSchema]
                        #RunstatOprObj_Tab = TabSchema + '.' + ProgTabName
                        ProgName = ProgName.upper()
                        RunstatOprObj_Tab = ProgName + ProgSuffix
                    except:
                        RunstatOprObj_Tab = 'None'

                    TmpValue = ""
                    try:
                        TmpValue = RunstatJobDict[RunstatOprObj_Tab]
                    except:
                        pass
                    if TmpValue:
                        RunstatJobDict[RunstatOprObj_Tab].append([JobID, CityRange, CodeCycle, TwiceFlag])
                    else:
                        RunstatJobDict[RunstatOprObj_Tab] = [JobID, CityRange, CodeCycle, TwiceFlag]

                if searchPID_LoadObj and searchPName_LoadObj:
                    RunstatOprObj_Tab = Param_value
                    RunstatOprObj_Tab = RunstatOprObj_Tab.replace('"','')
                    RunstatOprObj_Tab = RunstatOprObj_Tab.upper()
                    TmpValue = ""
                    try:
                        TmpValue = RunstatJobDict[RunstatOprObj_Tab]
                    except:
                        pass
                    if TmpValue == "":
                        RunstatJobDict[RunstatOprObj_Tab] = [JobID, CityRange, CodeCycle, TwiceFlag]

    return MaxRunstatJobID, RunstatJobDict, CodeIDDict, MaxDsID


def GetOldCtlConfDict(ExcelHandle, SheetDict):
    OldCtlConfDict = {}
    SheetNameList = ['CTL.JOB_PARAM_DEF', 'CTL.JOB_REF', 'CTL.JOB_OPR_OBJ', 'CTL.JOB_TIME_REF', 'CTL.JOB_WNMS']
    #print SheetNameList
    #sys.exit(1)

    for SheetName in SheetNameList:
        Sheet = ExcelHandle.sheet_by_name(SheetName)
        nrows = Sheet.nrows  #rows
        ncols = Sheet.ncols  #cols
        Cols  = [int(SheetDict[SheetID][1]) for SheetID in SheetDict if SheetDict[SheetID][0] == SheetName][0]
        OldCtlConfDict[SheetName] = []
        for LineID in range(0, nrows):
            rowvaluelist = Sheet.row_values(LineID)
            rowvaluelist = [re.sub(r'\.0.*$', "", str(value)) for value in rowvaluelist]
            OldCtlConfDict[SheetName].append(rowvaluelist[0:Cols])

    return OldCtlConfDict
    

def CtlConstruct(CodeConfDict, TemplateDict, CfgFileCfgDict, CtlExcelFullName, MaxRunstatJobID, RunstatJobDict, OldCtlConfDict):
    today = datetime.date.today()
    TodayStr = today.strftime("%Y.%m.%d")
    Author  = r'配置人：何平涛'
    ReqID   = CfgFileCfgDict['version'][0]
    ReqName = CfgFileCfgDict['version'][1]
    CtlConfDict = {}
    OldJobCtlConfDict = {}
    CodeConfList = []
    JobIDTwiceList = []
    for RowID in sorted(CodeConfDict):
        #print RowID
        CodeConfList = CodeConfDict[RowID]
        #print CodeConfList
        #sys.exit(1)
        IDType   = CodeConfList[0]
        CodeType = CodeConfList[1]
        CodeID = CodeConfList[2]
        CodeDesc  = CodeConfList[3]
        CodeDesc  = re.sub(r' |\n', '', CodeDesc)
        CodeDesc  = CodeDesc.encode('gbk')
        DsID  = ""
        JobID = ""
        CodeName = ""
        MaxRunstatJobID = MaxRunstatJobID + 1
        RunstatJobID = str(MaxRunstatJobID)
        if IDType == 'insert_update_job':
            JobID  = CodeID
            #CodeDesc  = CodeConfList[3]
            CodeName  = CodeConfList[4]
            searchOTNObj = re.search(r'^PRO_(.*)\.pl$', CodeName, re.I|re.M)
            TabName = ""
            if searchOTNObj: TabName = searchOTNObj.group(1)
            TabSchema = ProgSchemaDict[CodeType]
            CodeObjTabName = TabSchema + "." + TabName
            CityRange = CodeConfList[5]
            CodeCycle = CodeConfList[6]
            CodeCycle = CodeCycleDict[CodeCycle]
            CodeTabPart = CodeConfList[7]
            CodePreRef  = CodeConfList[8]
            CodeOprObj  = CodeConfList[9]
            #print CodeOprObj
        elif IDType == 'insert_update_ds':
            DsID  = CodeID
            DS_ID = DsID
            if len(DS_ID) == 3:
                DS_ID = "0" + DS_ID
            Cols      = CodeConfList[4]
            Delt      = CodeConfList[5]
            CodeName  = CodeConfList[6]
            CodeBaseName = CodeName
            if re.search(r'\(\$', CodeBaseName, re.I|re.M):
                CodeBaseName  = re.sub(r'\(|\)|\$', '', CodeBaseName)
            else:
                CodeName = re.sub(r'(YYYY|MM|DD)'      , r'($\1)'    , CodeBaseName)
                CodeName = re.sub(r'(HH|HR)'           , r'($SS)'    , CodeName)
                CodeName = re.sub(r'([\._])(S+)([\.])' , r'\1($\2)\3', CodeName)
                CodeName = re.sub(r'([\._])(N)([\.])'  , r'\1($S)\3' , CodeName)
            searchCompressObj = re.search(r'(\.Z|\.gz|\.zip|\.bz|\.bz2|\.7z)$', CodeBaseName, re.I|re.M)
            CompressType = "0"
            CompressTypeDesc = ""
            FileNameLength = "0"
            if searchCompressObj:
                CompressTypeDesc = searchCompressObj.group(1)
                if CompressTypeDesc == '.Z':
                    CompressType = "1"
                elif CompressTypeDesc == '.gz':
                    CompressType = "3"
            if CompressType == "0":
                FileNameLength = str(len(CodeBaseName))
                if CompressTypeDesc == '.zip':
                    FileNameLength = str(len(CodeBaseName[0:CodeBaseName.find(CompressTypeDesc)]))
            elif CompressType in ("1", "3"):
                FileNameLength = str(len(CodeBaseName[0:CodeBaseName.find(CompressTypeDesc)]))
                #print FileNameLength

            DsFileNameStr  = CodeName[0:CodeName.find('(')]
            Utf8_Flag      = CodeConfList[7]
            if Utf8_Flag == '是'.decode('gbk'):
                Utf8_Flag = "UTF8"
            else:
                Utf8_Flag = "None"
            Target_TabName = CodeConfList[8]
            StartDate      = re.sub(r'\.', '', TodayStr)
            CodeTabPart    = CodeConfList[9]
            Ds_Dir         = CodeConfList[10]
            Ds_Dir         = re.sub(r' */dxn1| */jkfile|/ *_EXF/*\s*', '', Ds_Dir)
            CodeCycle      = CodeConfList[11]
            #CodeCycle      = CodeCycleDict[CodeCycle.decode('gbk')]
            CodeCycle      = CodeCycleDict[CodeCycle]
            ARRIVE_DATE_FORMAT   = "Y:M:D"
            ARRIVE_DATE          = "1"
            EARLIEST_ARRIVE_TIME = ""
            LATEST_ARRIVE_TIME   = "Y:M:D+3 03:00:00"
            if CodeCycle == 'Day':
                CodeCycleID = "1"
                ARRIVE_DATE_FORMAT   = "Y:M:D"
                ARRIVE_DATE          = "1"
                EARLIEST_ARRIVE_TIME = ""
                LATEST_ARRIVE_TIME   = "Y:M:D+3 03:00:00"
            elif CodeCycle == 'Mon':
                CodeCycleID = "2"
                ARRIVE_DATE_FORMAT   = "Y:M:1"
                ARRIVE_DATE          = "6"
                EARLIEST_ARRIVE_TIME = "Y:M:D-1:h+01:m:s"
                LATEST_ARRIVE_TIME   = "Y:M+2:06 23:00:00"
            FileCntDesc      = CodeConfList[12]
            FileCount = ""
            List_FileName = ""
            try:
                FileCount = str(int(FileCntDesc))
            except:
                List_FileName = FileCntDesc

            DsCntType = "0"
            if List_FileName != "":
                DsCntType = "1"
                FileCount = "999999"
                if re.search(r'\(\$', List_FileName, re.I|re.M):
                    pass
                else:
                    List_FileName = re.sub(r'(YYYY)', r'($\1)', List_FileName)
                    List_FileName = re.sub(r'(MM)'  , r'($\1)', List_FileName)
                    List_FileName = re.sub(r'(DD)'  , r'($\1)', List_FileName)
                
            HeadRecoLineID = CodeConfList[13]
            if HeadRecoLineID in ('否'.decode('gbk'), '无'.decode('gbk')):
                HeadRecoLineID = "0"
            elif HeadRecoLineID in ('是'.decode('gbk'), '有'.decode('gbk')):
                HeadRecoLineID = "1"
            TailRecoLineID = "0"
            Skip = HeadRecoLineID
            #Ls_Update_JobID    = CodeConfList[17])
            IP_ADDR = "10.201.63.81"
            CNT_FLAG = "0"
            INST_DEF = "1"
            if FileCount == "1":
                CNT_FLAG  = "1"
            else:
                CNT_FLAG  = "0"
                if FileCount == "999999":
                    INST_DEF = ""
            INST_CNT  = FileCount
            CityRange = CodeConfList[16]
            #TPRsProgName     = TPRsProgDict[TPType][0]
            #RsDdateValidFlag = TPRsProgDict[TPType][1]

            ##encode
            #DsFileNameStr        = DsFileNameStr.encode('gbk')
            #Ds_Dir               = Ds_Dir.encode('gbk')
            #DS_ID                = DS_ID.encode('gbk')
            #IP_ADDR              = IP_ADDR.encode('gbk')
            #Cols                 = Cols.encode('gbk')
            #Delt                 = Delt.encode('gbk')
            #CompressType         = CompressType.encode('gbk')
            ##CodeName             = CodeName.encode('gbk')
            #Target_TabName       = Target_TabName.encode('gbk')
            ##CodeTabPart          = CodeTabPart.encode('gbk')
            #StartDate            = StartDate.encode('gbk')
            #HeadRecoLineID       = HeadRecoLineID.encode('gbk')
            #TailRecoLineID       = TailRecoLineID.encode('gbk')
            #CodeCycle            = CodeCycle.encode('gbk')
            #ARRIVE_DATE_FORMAT   = ARRIVE_DATE_FORMAT.encode('gbk')
            #ARRIVE_DATE          = ARRIVE_DATE.encode('gbk')
            #EARLIEST_ARRIVE_TIME = EARLIEST_ARRIVE_TIME.encode('gbk')
            #LATEST_ARRIVE_TIME   = LATEST_ARRIVE_TIME.encode('gbk')
        #OprObjTabName = TabSchema + "." + TabName
        UpdateCtlType = ""
        try:
            #UpdateCtlType = RunstatJobDict[CodeObjTabName]
            UpdateCtlType = RunstatJobDict[CodeName]
        except:
            pass
        #print CodeObjTabName

        if UpdateCtlType:
            OldCdJobID = RunstatJobDict[CodeName][0]
            JobID = OldCdJobID
            OldRsJobID = ""
            try:
                OldRsJobID = RunstatJobDict[CodeObjTabName][0]
            except:
                pass

            if OldRsJobID:
                OldJobID = [OldCdJobID, OldRsJobID]
            else:
                OldJobID = [OldCdJobID]
                
            for SheetName in OldCtlConfDict:
                OldJobCtlConfDict[SheetName] = []
                OldCtlConfList = OldCtlConfDict[SheetName]
                #print OldCtlConfList
                #sys.exit(1)
                for TmpCtlLine in OldCtlConfList:
                    TmpJobID = re.sub(r'\.0.*$', "", str(TmpCtlLine[0]))
                    if SheetName == 'CTL.JOB_WNMS':
                        if TmpJobID in OldJobID:
                            OldJobCtlConfDict[SheetName].append(TmpCtlLine)
                    else:
                        if TmpJobID == OldCdJobID:
                            OldJobCtlConfDict[SheetName].append(TmpCtlLine)
                        
            #print OldJobCtlConfDict
            #sys.exit(1)

        #print UpdateCtlType

        #if JobID == '12303257':
        #    CodeCycle = 'Day'
        #    print CodeCycle, Ref_CodeCycle
        #    #sys.exit(1)
        JobIDAttr = CityRange + CodeCycle
        RunstatOprObj_Tab = ""
        CodePreREF_JOB_ID = ""
        TPType = ""
        
        tmpCodeTabPart = CodeTabPart.encode('gbk')
        #searchTP_NoPObj  = re.search(r'3', CodeTabPart, re.I|re.M)
        searchTP_NoPObj2 = re.search(r'3|无|不', tmpCodeTabPart, re.I|re.M)
        #searchTP_DayPObj = re.search(r'0', CodeTabPart, re.I|re.M)
        searchTP_DayPObj2 = re.search(r'0|日', tmpCodeTabPart, re.I|re.M)
        #searchTP_MonPObj = re.search(r'1', CodeTabPart, re.I|re.M)
        searchTP_MonPObj2 = re.search(r'1|月', tmpCodeTabPart, re.I|re.M)
        #searchTP_ExpObj  = re.search(r'9', CodeTabPart, re.I|re.M)
        searchTP_ExpObj2  = re.search(r'3|无|不', tmpCodeTabPart, re.I|re.M)
        
        if searchTP_NoPObj2:   TPType = 'None'
        if searchTP_DayPObj2:  TPType = 'Day'
        if searchTP_MonPObj2:  TPType = 'Mon'
        if re.search(r'_EXP.pl$', CodeName, re.I|re.M) and searchTP_ExpObj2: TPType = 'Exp'
        print CodeName, CodeTabPart, TPType
        #print CodeTabPart, TPType
        #sys.exit(1)
        #CodeName = CodeName.encode('gbk')
        #CodePreREF_JOB_ID = CodePreREF_JOB_ID.encode('gbk')
        #RunstatOprObj_Tab = RunstatOprObj_Tab.encode('gbk')
        if TPType != 'Exp' and IDType in ('insert_update_ds', 'insert_update_job'):
            TPRsProgName     = TPRsProgDict[TPType][0]
            RsDdateValidFlag = TPRsProgDict[TPType][1]
            
            #print CodePreRef
            #sys.exit(1)
            if IDType in ('insert_update_job'):
                #print CodeOprObj
                OprObjTabName = [tmpOprObjTabName for tmpOprObjTabName in CodeOprObj if re.search(r'^(.*)\(1\)$', tmpOprObjTabName, re.I|re.M)][0]
                searchOprObj  = re.search(r'^(.*)\(([0-9])\)$', OprObjTabName, re.I|re.M)
                OprObjTabName = searchOprObj.group(1)
                #OprObj_Type = searchOprObj.group(2)
                #OprObj_Tab  = '"' + OprObj_Tab + '"'
                #OprObjTabName = OprObjTabName.encode('gbk')
                #print RunstatJobID
                try:
                    RunstatJobID = RunstatJobDict[OprObjTabName][0]
                except:
                    pass

            if IDType in ('insert_update_ds'):
                #OprObj_Type = searchOprObj.group(2)
                #OprObj_Tab  = '"' + OprObj_Tab + '"'
                #OprObjTabName = OprObjTabName.encode('gbk')
                #print RunstatJobID
                try:
                    RunstatJobID = RunstatJobDict[Target_TabName][0]
                except:
                    pass
                #print RunstatJobID
                #print RunstatJobDict[OprObjTabName][0]
                #sys.exit(1)
                #RunstatJobDict[CodeObjTabName] = [RunstatJobID, CityRange, CodeCycle]
                #RunstatJobDict[RunstatOprObj_Tab] = [JobID, CityRange, CodeCycle]

                #print TemplateDict[IDType]
                #print IDType

                #CodeName = CodeName.encode('gbk')
                #CodePreREF_JOB_ID = CodePreREF_JOB_ID.encode('gbk')
                #TPRsProgName = TPRsProgName.encode('gbk')
                #RunstatOprObj_Tab = RunstatOprObj_Tab.encode('gbk')

        LineID = 0
        CtlConfList = []
        JobIDTwiceList = []
        OldCtlConfList = []
        TimeRefList = []
        DS_JobIDList = []
        Ref_JobTwiceCnt = 0
        print "\n" + CodeName + "\n"
        for LineList in TemplateDict[IDType]:
            Diff_Cnt = 0
            LineID = LineID + 1
            SheetName = LineList[0]
            ConfType  = LineList[1]
            #del LineList[0], LineList[0]
            #print SheetName
            #print LineList[2:]
            OldJobCtlConfList = []
            if UpdateCtlType:
                if SheetName in ('CTL.JOB_DEF'):
                    continue
                else:
                    try:
                        OldJobCtlConfList = OldJobCtlConfDict[SheetName]
                    except:
                        pass
                #print OldJobCtlConfList
                #sys.exit(1)
                
            TmpValue = ""
            try:
                TmpValue = CtlConfDict[SheetName]
            except:
                pass
            #print TmpValue
            if TmpValue == "":
                if UpdateCtlType == "":
                    CtlConfDict[SheetName] = [[TodayStr, ReqID, ReqName, Author]]
                else:
                    CtlConfDict[SheetName] = []
            #print TmpValue
                    
            CtlConfList = LineList[2:]
            if ConfType == "CODE":
                if IDType == 'insert_update_job':
                    CtlConfList[0] = JobID
                elif IDType == 'insert_update_ds' and SheetName in ('CTL.TA_ETL_DS_DEF', 'CTL.TA_ETL_DS_HOST', 'CTL.TA_ETL_LOAD_CTRL', 'CTL.TA_ETL_QUALITY_CONTROL', 'CTL.DS_CNT_DEF', 'CTL.DATA_CLEAR_RULES'):
                    CtlConfList[0] = DsID
                if SheetName == 'CTL.JOB_REF' and IDType == 'insert_update_job':
                    CtlConfList = []
                    Ref_JobTwiceFlag = "0"
                    TwiceList = []
                    NoTwiceList = []
                    Ref_Flag = 0
                    Ref_Cnt = len(CodePreRef)
                    Ref_ID = 0
                    for Ref_OprObj in CodePreRef:
                        Ref_ID = Ref_ID + 1
                        Ref_TabName = Ref_OprObj[Ref_OprObj.find(".") + 1:]
                        Ref_CodeName = "PRO_" + Ref_TabName + ".pl"
                        if TPType != 'Exp':
                            if Ref_OprObj == OprObjTabName:
                                if CodeCycle == 'Day':
                                    Ref_Level = "1011"
                                elif CodeCycle == 'Mon':
                                    Ref_Level = "1021"
                                    CtlConfLine = [JobID, RunstatJobID, '0', Ref_Level, '']
                                    TimeRefList.append(CtlConfLine)
                                    continue

                        Ref_OprObj_JobID = ""
                        Ref_CodeName_JobID = ""
                        try:
                            Ref_OprObj_JobID = RunstatJobDict[Ref_OprObj]
                        except:
                            pass
                        try:
                            Ref_CodeName_JobID = RunstatJobDict[Ref_CodeName]
                        except:
                            pass
                        #print Ref_OprObj
                        #print TmpValue1
                        #print TmpValue2
                        #sys.exit(1)
                        Ref_JobID = ""
                        print CodeName, Ref_OprObj
                        Ref_CodeCycle = ""
                        Ref_JobIDAttr = ""
                        Ref_Desc  = ""
                        Ref_Level = ""
                        if Ref_OprObj_JobID:
                            Ref_JobID = RunstatJobDict[Ref_OprObj][0]
                            Ref_CityRange = RunstatJobDict[Ref_OprObj][1]
                            Ref_CodeCycle = RunstatJobDict[Ref_OprObj][2]
                            Ref_JobTwiceFlag = RunstatJobDict[Ref_OprObj][3]
                            #Ref_JobIDAttr = Ref_CityRange + Ref_CodeCycle
                            #Ref_Desc  = JobIDAttr + ":" + Ref_JobIDAttr
                        elif Ref_CodeName_JobID:
                            try:
                                Ref_JobID = RunstatJobDict[CodeName][0]
                                Ref_CityRange = RunstatJobDict[CodeName][1]
                                Ref_CodeCycle = RunstatJobDict[CodeName][2]
                                Ref_JobTwiceFlag = RunstatJobDict[CodeName][3]
                                #Ref_JobIDAttr = Ref_CityRange + Ref_CodeCycle
                                #Ref_Desc  = JobIDAttr + ":" + Ref_JobIDAttr
                            except:
                                Ref_JobIDList = [JobInfo[0] for JobInfo in RunstatJobDict[CodeName]]
                                Ref_JobTwiceFlagList = [JobInfo[3] for JobInfo in RunstatJobDict[CodeName]]
                                print "\n".join(Ref_JobIDList)
                                Select_Job = raw_input("Which job would you like to follow below?")
                                if Select_Job:
                                    Ref_JobID = Select_Job
                                    Ref_CityRange = [JobInfo[1] for JobInfo in RunstatJobDict[CodeName] if JobInfo[0] == Ref_JobID][0]
                                    Ref_CodeCycle = [JobInfo[2] for JobInfo in RunstatJobDict[CodeName] if JobInfo[0] == Ref_JobID][0]
                                    Ref_JobTwiceFlag = [JobInfo[3] for JobInfo in RunstatJobDict[CodeName] if JobInfo[0] == Ref_JobID][0]
                                    #Ref_JobIDAttr = Ref_CityRange + Ref_CodeCycle
                                else:
                                    Ref_JobID = RunstatJobDict[CodeName][0][0]
                                    Ref_CityRange = RunstatJobDict[CodeName][0][1]
                                    Ref_CodeCycle = RunstatJobDict[CodeName][0][2]
                                    Ref_JobTwiceFlag = RunstatJobDict[CodeName][0][3]
                        else:
                            if (Ref_Flag == 0 and Ref_ID == Ref_Cnt) or Ref_Cnt == 1:
                                #print Ref_OprObj + " has no ctl job, please verify it!"
                                print "All the ref operating objects have no ctl job, please verify it!"
                                continue_flag = raw_input("Do you want to continue? yes or no?")
                                if re.search(r'^n(o)?$', continue_flag, re.I|re.M):
                                    sys.exit(1)
                                else:
                                    Ref_JobID     = '11000120'
                                    Ref_CityRange = "Gmcc"
                                    Ref_CodeCycle = "Day"
                                    #Ref_JobIDAttr = "GmccDay"
                                    #Ref_Desc      = JobIDAttr + ":" + Ref_JobIDAttr
                                    #break
                            else:
                                print CodeName, Ref_OprObj + " has no ctl job, please verify it!"
                                continue_flag = raw_input("Do you want to continue? yes or no?")
                                if re.search(r'^n(o)?$', continue_flag, re.I|re.M):
                                    sys.exit(1)
                                else:
                                    continue

                        Ref_JobIDAttr = Ref_CityRange + Ref_CodeCycle
                        Ref_Desc  = JobIDAttr + ":" + Ref_JobIDAttr
                        try:
                            Ref_Level = CodeRefDict[Ref_Desc]
                        except:
                            pass

                        if Ref_Level:
                            Ref_Flag = 1
                        else:
                            Ref_Level = Ref_Desc
              
                        #print Ref_OprObj, Ref_Level
                        #print Ref_JobID
                        #print [JobID, Ref_JobID, '1', '0', '']
                        #CtlConfList.append([JobID, Ref_JobID, '1', '0', ''])
                        if Ref_Level == '1' and re.search(r'^11[0-9]{4}60$', Ref_JobID, re.I|re.M):
                            Ref_Level = '2'

                        #print Ref_JobTwiceFlag
                        if Ref_JobTwiceFlag == "1":
                            CtlConfLine = [JobID, Ref_JobID, Ref_Level, '0', '']
                            TwiceList.append(CtlConfLine)
                            Ref_JobTwiceCnt = Ref_JobTwiceCnt + 1

                        if Ref_JobTwiceFlag == "0":
                            if Ref_JobTwiceCnt > 0:
                                if CodeCycle in ("Day", "Week"):
                                    Ref_Level = "1111"
                                elif CodeCycle == "Mon":
                                    Ref_Level = "1121"
                                else:
                                    Ref_Level = Ref_Desc
                            CtlConfLine = [JobID, Ref_JobID, '0', Ref_Level, '']
                            NoTwiceList.append(CtlConfLine)

                        CtlConfLine = [JobID, Ref_JobID, Ref_Level, '0', '']
                        #print CtlConfLine
                        if CodeCycle == 'Day' and Ref_CodeCycle == 'Mon':
                            #TimeRefList.append([JobID, Ref_JobID, '1', '0', ''])
                            TimeRefList.append(CtlConfLine)
                            #print TimeRefList
                            #sys.exit(1)
                        else:
                            #CtlConfList.append([JobID, Ref_JobID, Ref_Level, '0', ''])
                            CtlConfList.append(CtlConfLine)

                    if Ref_JobTwiceCnt > 0:
                        #print TwiceList
                        #sys.exit(1)
                        CtlConfList = TwiceList
                        TimeRefList = NoTwiceList
                        #print CtlConfList
                        #CtlConfList.append(CtlConfLine)
                        #RunstatJobDict[CodeObjTabName] = [RunstatJobID, CityRange, CodeCycle, "1"]
                        JobIDTwiceList.append([JobID])
                        JobIDTwiceList.append([RunstatJobID])

                    #print CtlConfList
                    CodePreREF_JOB_ID = CtlConfList[0][1]
                    PreREF_JOB_IDList = [line[1] for line in CtlConfList]
                    #print CodePreREF_JOB_ID
                    #sys.exit(1)

                    #print CtlConfList
                    if UpdateCtlType:
                        Diff_Cnt = CompareNewOld(SheetName, CtlConfList, OldJobCtlConfList)

                if SheetName == 'CTL.JOB_TIME_REF':
                    TmpValue = ""
                    try:
                        TmpValue = CtlConfDict[SheetName]
                    except:
                        pass
                    #print TmpValue
                    if TimeRefList :
                        #print TimeRefList
                        CtlConfList = []
                        for tmpTimeRefList in TimeRefList:
                            CtlConfList.append(tmpTimeRefList)
                    else:
                        if TmpValue:
                            CtlConfList = [[]]
                        else:
                            del CtlConfDict[SheetName]
                            print "Fuck"
                        #if UpdateCtlType == "":
                        #    del CtlConfDict[SheetName]
                        #else:
                        #    pass
                    #print CtlConfList

                    if UpdateCtlType:
                        if CtlConfList == [[]]:
                            CtlConfList = []
                        Diff_Cnt = CompareNewOld(SheetName, CtlConfList, OldJobCtlConfList)
                        #print Ref_JobTwiceCnt

                if SheetName == 'CTL.JOB_WNMS':
                    TmpValue = ""
                    try:
                        TmpValue = CtlConfDict[SheetName]
                    except:
                        pass
                    #print TmpValue
                    if JobIDTwiceList:
                        #print JobIDTwiceList
                        CtlConfList = []
                        for tmpJobID in JobIDTwiceList:
                            CtlConfList.append(tmpJobID)
                    else:
                        if TmpValue:
                            CtlConfList = [[]]
                        else:
                            del CtlConfDict[SheetName]
                            print "Fuck"

                    if UpdateCtlType:
                        if CtlConfList == [[]]:
                            CtlConfList = []
                        Diff_Cnt = CompareNewOld(SheetName, CtlConfList, OldJobCtlConfList)

                if SheetName == 'CTL.JOB_OPR_OBJ':
                    if IDType == 'insert_update_job':
                        CtlConfList = []
                        #print CodeOprObj
                        for OprObj in CodeOprObj:
                            print OprObj
                            searchOprObj = re.search(r'^(.*?)\(([0-9])\)$', OprObj, re.I|re.M)
                            if searchOprObj:
                                OprObj_Tab  = searchOprObj.group(1)
                                OprObj_Type = searchOprObj.group(2)
                            else:
                                OprObj_Tab  = OprObj
                                OprObj_Type = "0"
                            OprObj_Tab  = '"' + OprObj_Tab + '"'
                            if OprObj_Type == "1":
                                RunstatOprObj_Tab = OprObj_Tab.replace('"','')
                                #RunstatOprObj_Tab = RunstatOprObj_Tab.encode('gbk')
                            OprObj_Type  = '"' + OprObj_Type + '"'
                            CtlConfList.append([JobID, OprObj_Tab, OprObj_Type])
                    elif IDType == 'insert_update_ds':
                        CtlConfList[0] = re.sub(r'DS_ID'         , DS_ID         , CtlConfList[0])
                        CtlConfList[1] = re.sub(r'Target_TabName', Target_TabName, CtlConfList[1])
                        CtlConfList = [CtlConfList]

                    if UpdateCtlType:
                        Diff_Cnt = CompareNewOld(SheetName, CtlConfList, OldJobCtlConfList)

            #print CtlConfDict
            if ConfType == "RUNSTATS" and TPType == 'Exp':
                continue
            if ConfType == "RUNSTATS" and TPType != 'Exp':
                #print CodeObjTabName
                #sys.exit(1)
                CtlConfList[0] = RunstatJobID
                #print RunstatJobID
                #sys.exit(1)
                #CtlConfList[1] = re.sub(r'REF_JOB_ID', JobID, CtlConfList[1])
                #RunstatJobDict[RunstatOprObj_Tab] = [RunstatJobID, CityRange, CodeCycle, "0"]
                if SheetName == 'CTL.JOB_REF':
                    #pass
                    #CtlConfList = [RunstatJobID, JobID, '1', '0', '']
                    if IDType == 'insert_update_job':
                        CtlConfList[1:] = [JobID, '1', '0', '']
                    elif IDType == 'insert_update_ds':
                        CtlConfList[1] = re.sub(r'DS_ID', DS_ID, CtlConfList[1])
                if SheetName == 'CTL.JOB_OPR_OBJ':
                    if IDType == 'insert_update_ds':
                        RunstatOprObj_Tab = Target_TabName
                    CtlConfList[1:] = ['"' + RunstatOprObj_Tab + '"', '"1"']
                    TwiceFlag = ""
                    if Ref_JobTwiceCnt <= 0:
                        TwiceFlag = "0"
                    elif Ref_JobTwiceCnt > 0:
                        TwiceFlag = "1"
                    RunstatJobDict[RunstatOprObj_Tab] = [RunstatJobID, CityRange, CodeCycle, TwiceFlag]

            if SheetName == 'CTL.TA_ETL_DS_DEF':
                CtlConfList[1]  = re.sub(r'DS_NAME'             , CodeDesc            , CtlConfList[1] )
                CtlConfList[3]  = re.sub(r'Cols'                , Cols                , CtlConfList[3] )
                CtlConfList[4]  = re.sub(r'Delt'                , Delt                , CtlConfList[4] )
                CtlConfList[5]  = re.sub(r'CompressType'        , CompressType        , CtlConfList[5] )
                CtlConfList[6]  = re.sub(r'Ds_FileName'         , CodeName            , CtlConfList[6] )
                CtlConfList[7]  = re.sub(r'Target_TabName'      , Target_TabName      , CtlConfList[7] )
                CtlConfList[9]  = re.sub(r'StartDate'           , StartDate           , CtlConfList[9] )
                CtlConfList[11] = re.sub(r'HeadRecoLineID'      , HeadRecoLineID      , CtlConfList[11])
                CtlConfList[12] = re.sub(r'TailRecoLineID'      , TailRecoLineID      , CtlConfList[12])
                CtlConfList[13] = re.sub(r'Ds_Dir'              , Ds_Dir              , CtlConfList[13])
                CtlConfList[14] = re.sub(r'DS_ID'               , DS_ID               , CtlConfList[14])
                CtlConfList[15] = re.sub(r'DsCntType'           , DsCntType           , CtlConfList[15])
                CtlConfList[16] = re.sub(r'List_FileName'       , List_FileName       , CtlConfList[16])
                CtlConfList[17] = re.sub(r'DS_ID'               , DS_ID               , CtlConfList[17])
                if List_FileName: 
                    CtlConfList[17] = re.sub(r'^"(.*)"$'        , r'"(\1)"'           , CtlConfList[17])
                CtlConfList[18] = re.sub(r'CodeCycleID'         , CodeCycleID         , CtlConfList[18])
                CtlConfList[20] = re.sub(r'ARRIVE_DATE_FORMAT'  , ARRIVE_DATE_FORMAT  , CtlConfList[20])
                CtlConfList[21] = re.sub(r'ARRIVE_DATE'         , ARRIVE_DATE         , CtlConfList[21])
                CtlConfList[22] = re.sub(r'EARLIEST_ARRIVE_TIME', EARLIEST_ARRIVE_TIME, CtlConfList[22])
                CtlConfList[23] = re.sub(r'LATEST_ARRIVE_TIME'  , LATEST_ARRIVE_TIME  , CtlConfList[23])
                CtlConfList[26] = re.sub(r'Ds_Dir'              , Ds_Dir              , CtlConfList[26])
                CtlConfList[27] = re.sub(r'Ds_Dir'              , Ds_Dir              , CtlConfList[27])
                CtlConfList[28] = re.sub(r'Ds_Dir'              , Ds_Dir              , CtlConfList[28])

            if SheetName == 'CTL.TA_ETL_DS_HOST' or SheetName == 'CTL.TA_ETL_LOAD_CTRL':
                CtlConfList[1]  = re.sub(r'IP_ADDR', IP_ADDR, CtlConfList[1] )

            if SheetName == 'CTL.DS_CNT_DEF':
                CtlConfList[2]  = re.sub(r'FileCount', FileCount, CtlConfList[2])
                CtlConfList[3]  = re.sub(r'FileCount', FileCount, CtlConfList[3])
                CtlConfList[4]  = re.sub(r'IP_ADDR'  , IP_ADDR  , CtlConfList[4])
                CtlConfList[5]  = re.sub(r'DS_ID'    , DsID     , CtlConfList[5])

            if SheetName == 'CTL.DATA_CLEAR_RULES':
                if ConfType == 'NUTF8' and Utf8_Flag == 'UTF8':
                    del CtlConfDict[SheetName]
                    continue

                CtlConfList[0] = re.sub(r'DsID'         , DsID         , CtlConfList[0])
                CtlConfList[4] = re.sub(r'Ds_Dir'       , Ds_Dir       , CtlConfList[4])
                CtlConfList[4] = re.sub(r'DsFileNameStr', DsFileNameStr, CtlConfList[4])

            if SheetName == 'CTL.JOB_LEVEL_CTRL':
                CtlConfList[0] = re.sub(r'DS_ID'  , DS_ID  , CtlConfList[0])
                #CtlConfList[0]  = re.sub(DsID       , "11"+DS_ID+"60", CtlConfList[0])
                CtlConfList[3]  = re.sub(r'CNT_FLAG', CNT_FLAG, CtlConfList[3])
                CtlConfList[4]  = re.sub(r'INST_CNT', INST_CNT, CtlConfList[4])
                CtlConfList[5]  = re.sub(r'INST_DEF', INST_DEF, CtlConfList[5])
                CtlConfList[6]  = re.sub(r'IP_ADDR' , IP_ADDR , CtlConfList[6])

            if SheetName == 'CTL.JOB_DEF':
                if ConfType == 'UTF8' and Utf8_Flag == 'None':
                    continue

                if ConfType == 'NUTF8' and Utf8_Flag == 'UTF8':
                    continue

                if ConfType == 'UTF8' and Utf8_Flag == 'UTF8' and CompressTypeDesc == "" and CtlConfList[0] == '11DS_ID30':
                    continue

                CtlConfList[2] = re.sub(r'CodeDesc', CodeDesc, CtlConfList[2])
                #print CtlConfList[2]
                #sys.exit(1)
                if ConfType in ['UTF8', 'NUTF8']:
                    CtlConfList[0] = re.sub(r'DS_ID'  , DS_ID  , CtlConfList[0])
                    CtlConfList[1] = re.sub(r'IP_ADDR', IP_ADDR, CtlConfList[1])
                    DS_JobID = CtlConfList[0]
                    DS_JobIDList.append(DS_JobID)

            if SheetName == 'CTL.JOB_REF' and ConfType == "CODE" and IDType == 'insert_update_ds':
                #tmpCtlConfList = []
                #tmpCtlConfList = CtlConfList
                CtlConfList = []
                DS_RefJobIDDict = {}
                if len(DS_JobIDList) >= 2:
                    ID = 1
                    for tmpJobID in DS_JobIDList[1:]:
                        JOB_ID     = DS_JobIDList[ID]
                        REF_JOB_ID = DS_JobIDList[ID - 1]
                        #tmpCtlConfList[0] = JOB_ID
                        #tmpCtlConfList[1] = REF_JOB_ID
                        #CtlConfList.append(tmpCtlConfList)
                        Ref_Level = '1'
                        if re.search(r'^11[0-9]{4}60$', REF_JOB_ID, re.I|re.M):
                            Ref_Level = '2'
                        CtlConfList.append([JOB_ID, REF_JOB_ID, Ref_Level, '0', ''])
                        DS_RefJobIDDict[JOB_ID] = REF_JOB_ID
                        ID = ID + 1

            if SheetName == 'CTL.JOB_PARAM_DEF':
                #if UpdateCtlType:
                #    continue
                #pass
                #print CodeName, CodePreREF_JOB_ID
                #print CtlConfList
                #sys.exit(1)
                if ConfType == 'UTF8' and Utf8_Flag == 'None':
                    continue

                if ConfType == 'NUTF8' and Utf8_Flag == 'UTF8':
                    continue

                if ConfType == 'UTF8' and Utf8_Flag == 'UTF8' and CompressTypeDesc == "" and CtlConfList[0] == '11DS_ID30':
                    continue

                if CodeCycle == 'Mon' and CtlConfList[1] == '"datadate"':
                    CtlConfList[6] = re.sub('datadate', 'datadate[0,6]', CtlConfList[6])
                    
                if ConfType in ("UTF8", "NUTF8"):
                    CtlConfList[0] = re.sub(r'DS_ID', DS_ID, CtlConfList[0])
                    if CtlConfList[0] != '11DS_ID01':
                        JOB_ID = CtlConfList[0]
                        REF_JOB_ID = ""
                        try:
                            REF_JOB_ID = DS_RefJobIDDict[JOB_ID]
                        except:
                            pass
                        CtlConfList[6] = re.sub('Ds_Dir'        , Ds_Dir        , CtlConfList[6])
                        CtlConfList[6] = re.sub('REF_JOB_ID'    , REF_JOB_ID    , CtlConfList[6])
                        CtlConfList[6] = re.sub(r'DS_ID'         , DS_ID         , CtlConfList[6])
                        CtlConfList[6] = re.sub(r'DsID'          , DsID          , CtlConfList[6])
                        CtlConfList[6] = re.sub(r'CompressType'  , CompressType  , CtlConfList[6])
                        CtlConfList[6] = re.sub('Target_TabName', Target_TabName, CtlConfList[6])
                        CtlConfList[6] = re.sub(r'Delt'          , Delt          , CtlConfList[6])
                        CtlConfList[6] = re.sub(r'Skip'          , Skip          , CtlConfList[6])
                        CtlConfList[6] = re.sub('#FileNameLength', "," + FileNameLength, CtlConfList[6])

                if ConfType == "CODE":
                    CtlConfList[6] = re.sub(r'CodeName', CodeName, CtlConfList[6])
                    CtlConfList[6] = re.sub('CodePreREF_JOB_ID', CodePreREF_JOB_ID, CtlConfList[6])

                if ConfType == "RUNSTATS" and TPType != 'Exp':
                    #print CtlConfList[6]
                    CtlConfList[6] = re.sub(r'TPRsProgName', TPRsProgName, CtlConfList[6])
                    CtlConfList[6] = re.sub('RunstatOprObj_Tab', RunstatOprObj_Tab, CtlConfList[6])
                    #print JobID
                    CtlConfList[6] = re.sub('CodePreREF_JOB_ID', JobID, CtlConfList[6])
                    CtlConfList[2] = re.sub('RsDdateValidFlag', RsDdateValidFlag, CtlConfList[2])
                    if IDType == 'insert_update_ds':
                        CtlConfList[6] = re.sub(r'DS_ID', DS_ID, CtlConfList[6])
                #print CtlConfList[6]
                if UpdateCtlType and IDType == 'insert_update_job' and ConfType == "CODE" and CtlConfList[1] == '"datadate"':
                    #print CtlConfList
                    #sys.exit(1)
                    #print SheetName
                    #print OldJobCtlConfList
                    #print CtlConfList
                    OldDatadateLine = [line for line in OldJobCtlConfList if line[1] == '"datadate"'][0]
                    #print OldDatadateLine
                    #NewDatadateLine = [line for line in CtlConfList if line[1] == '"datadate"']
                    NewDatadateLine = CtlConfList
                    #print NewDatadateLine                   
                    #sys.exit(1)
                    Pvalue = OldDatadateLine[6]
                    searchPvalue = re.search('([0-9]{8})', Pvalue, re.I|re.M)
                    PreREF_JOB_ID = ""
                    if searchPvalue:
                        PreREF_JOB_ID = searchPvalue.group(1)
                        if PreREF_JOB_ID not in PreREF_JOB_IDList:
                            Diff_Cnt = Diff_Cnt + 1
                            print "\n=====================" + SheetName + " need to update========="
                            print "====Old"
                            for tmp in OldDatadateLine:
                                #tmp = tmp.encode('gbk')
                                print tmp,
                            print "\n====New"
                            for tmp in NewDatadateLine:
                                print tmp,
                            #print "\n"
                        else:
                            print "\nThe configuration in " + SheetName + " of code " + CodeName + " " + OldCdJobID + " has no changing!"
                            
            if UpdateCtlType and Diff_Cnt == 0:
                if SheetName in ('CTL.JOB_REF', 'CTL.JOB_TIME_REF', 'CTL.JOB_OPR_OBJ') and ConfType != 'RUNSTATS':
                    print "\nThe configuration in " + SheetName + " of code " + CodeName + " " + OldCdJobID + " has no changing!"
                #CtlConfDict = {}
                #continue
                #sys.exit(0)

            TmpValue = ""
            try:
                TmpValue = CtlConfDict[SheetName]
            except:
                pass

            #print CtlConfDict
            #print SheetName
            #print TmpValue
            #if ConfType == "CODE" and SheetName in ['CTL.JOB_REF', 'CTL.JOB_TIME_REF', 'CTL.JOB_OPR_OBJ']:
            #    #and len(CtlConfList) >= 2
            #    for tmpCtlConfList in CtlConfList:
            #        if tmpCtlConfList:
            #            CtlConfDict[SheetName].append(tmpCtlConfList)
            #else:
            #    CtlConfDict[SheetName].append(CtlConfList)

            if TmpValue == [] or TmpValue:
                if ConfType == "CODE" and SheetName in ['CTL.JOB_REF', 'CTL.JOB_TIME_REF', 'CTL.JOB_OPR_OBJ', 'CTL.JOB_WNMS']:
                    #and len(CtlConfList) >= 2
                    for tmpCtlConfList in CtlConfList:
                        if tmpCtlConfList:
                            CtlConfDict[SheetName].append(tmpCtlConfList)
                else:
                    CtlConfDict[SheetName].append(CtlConfList)
            #else:
            #    CtlConfDict[SheetName].append(CtlConfList)
                
        #if UpdateCtlType:
        #    #OldJobID = RunstatJobDict[CodeObjTabName][0]
        #    OldCtlConfDict
    #print CtlConfDict
    #sys.exit(1)
    return CtlConfDict


def CompareNewOld(SheetName, CtlConfList, OldJobCtlConfList):
    #print CtlConfList
    #print OldJobCtlConfList
    NewLen = len(CtlConfList)
    OldLen = len(OldJobCtlConfList)
    #print NewLen, OldLen
    Diff_Cnt = 0
    if NewLen != OldLen:
        Diff_Cnt = 1
        #print "New":
        #print CtlConfList
        #print "Old":
        #print OldJobCtlConfList
    #else:
    NewConfList = []
    OldConfList = []
    TmpCtlConfList = []
    for TmpList in CtlConfList:
        #TmpList = [x.encode('gbk') for x in TmpList]
        TmpCtlConfList.append(TmpList)
    CtlConfList = TmpCtlConfList
    #print CtlConfList
    #print OldJobCtlConfList
    #sys.exit(1)
    for TmpCtlLine in CtlConfList:
        if TmpCtlLine not in OldJobCtlConfList:
            #print "New", TmpCtlLine
            NewConfList.append(TmpCtlLine)
            #print "Old", OldJobCtlConfList
            #OldConfList.append(OldJobCtlConfList)
            Diff_Cnt = Diff_Cnt + 1
        else:
            pass

    if Diff_Cnt >= 1 and NewConfList:
        print "\n=====================" + SheetName + " need to add========="
        for tmp in NewConfList:
            print ",".join(tmp)

    for TmpCtlLine in OldJobCtlConfList:
        if TmpCtlLine not in CtlConfList:
            #print "Old", TmpCtlLine
            OldConfList.append(TmpCtlLine)
            #print "New", CtlConfList
            #NewConfList.append(CtlConfList)
            Diff_Cnt = Diff_Cnt + 1
        else:
              pass

    if Diff_Cnt >= 1 and OldConfList:
        print "\n=====================" + SheetName + " need to remove========="
        for tmp in OldConfList:
            print ",".join(tmp)

    return Diff_Cnt


def main():

    CfgFileDict = {}

    ##Reading configure info based on excel document
    (CfgFileDict, CfgFileCfgDict)= ReadCfgFileCfgInfo(CfgFile)
    #print CfgFileDict
    #print CfgFileCfgDict
    #for cfg in CfgFileDict:
    #    print cfg, CfgFileDict[cfg]
    #sys.exit(0)

    ReqID = CfgFileCfgDict['version'][0]
    #print ReqID
    #print OutputPath
    CtlCfgFile = OutputPath + "/" + ReqID + ".cfg"
    #print CtlCfgFile

    #print type(CtlExcelFullName)
    print CtlExcelFullName
    #sys.exit(1)

    TemplateDict = GetTemplateDict(TemplateFile)
    ExcelHandle  = OpenExcel(CtlExcelFullName)
    SheetDict    = GetSheetInfo(CtlTableList)
    (MaxRunstatJobID, RunstatJobDict, CodeIDDict, MaxDsID) = GetJobInfo(ExcelHandle, SheetDict)
    OldCtlConfDict   = GetOldCtlConfDict(ExcelHandle, SheetDict)
    LatestCodeIDDict = GetLatestCodeID(LatestCodeIDFile, CodeIDDict, MaxDsID)
    CodeConfDict = {}
    #print SheetName
    CodeNameDict = {}
    IDCodeDict   = {}
    IDCodeDict['insert_update_ds']  = CfgFileCfgDict['insert_update_ds']
    IDCodeDict['insert_update_job'] = CfgFileCfgDict['insert_update_job']
    for IDType in IDCodeDict:
        searchDsObj  = re.search(r'_ds$',  IDType, re.I|re.M)
        searchJobObj = re.search(r'_job$', IDType, re.I|re.M)
        IDCodeList = IDCodeDict[IDType]
        for IDCode in IDCodeList:
            CodeID   = IDCode[0]
            CodeName = ""
            try:
                CodeName = IDCode[1]
            except:
                pass
            #print CodeID, CodeName
            if CodeName == "":
                CodeName = CodeID
                CodeName = CodeName.strip()
                CodeID = ""
                try:
                    CodeID = RunstatJobDict[CodeName]
                except:
                    pass

                if CodeID == "":
                    TmpValue = 0
                    CodeType = ""
                    if searchJobObj:
                        searchCodeObj = re.search(r'^PRO_([A-Z]+)_.*$', CodeName, re.I|re.M)
                        CodeType = searchCodeObj.group(1)
                    elif searchDsObj:
                        CodeType = 'DS'

                    #print CodeType
                    #print LatestCodeIDDict[CodeType]
                    try:
                        TmpValue = LatestCodeIDDict[CodeType]
                    except:
                        TmpValue = 0

                    TmpValue2 = 0
                    try:
                        TmpValue2 = CodeIDDict[TmpValue]
                    except:
                        pass
                    
                    while TmpValue2 == 1:
                        TmpValue = TmpValue + 1
                        try:
                            TmpValue2 = CodeIDDict[TmpValue]
                        except:
                            TmpValue2 = 0
                    CodeID = TmpValue
                    CodeIDDict[CodeID] = 1

                    try:
                        LatestCodeIDDict[CodeType] = CodeID
                    except:
                        print "What's up???"
                        pass
                    #print LatestCodeIDDict[CodeType]

            CodeNameDict[CodeName] = str(CodeID)

    for CfgInfo in CfgInfoList:
        ExcelFile = CfgInfo[0]
        SheetName = CfgInfo[1]
        print type(ExcelFile)
        ExcelFile = ExcelFile.decode('gbk').encode('utf-8')
        print type(SheetName)
        #ExcelFile = os.path.normcase(ExcelFile.encode('UTF-8'))
        ExcelHandle  = OpenExcel(ExcelFile)
        SheetName = SheetName.decode('gbk').encode('utf-8')
        SheetName = SheetName.strip()
        print ExcelFile
        print SheetName
        print type(ExcelFile)
        #sys.exit(1)
        tmpCodeConfDict = ReadExcel(ExcelHandle, SheetName, CfgFileCfgDict, CodeNameDict)
        if tmpCodeConfDict:
            for RowID in tmpCodeConfDict:
                CodeConfDict[RowID] = tmpCodeConfDict[RowID]

    CtlConfDict = CtlConstruct(CodeConfDict, TemplateDict, CfgFileCfgDict, CtlExcelFullName, MaxRunstatJobID, RunstatJobDict, OldCtlConfDict)
    #print CtlConfDict
    #SheetDict = GetSheetInfo(CtlTableList)
    insert_update_job_flag = ""
    try:
        insert_update_job_flag = CtlConfDict['CTL.JOB_DEF']
    except:
        pass

    insert_update_ds_flag = ""
    try:
        insert_update_ds_flag = CtlConfDict['CTL.TA_ETL_DS_DEF']
    except:
        pass

    try:
        os.remove(CtlCfgFile)
    except OSError:
        pass

    f = open(CtlCfgFile, "a")
    for lineID in sorted(CfgFileDict):
        #print type(CfgFileDict[lineID])
        #f.write(CfgFileDict[lineID][0])
        #print lineID
        CfgValueStr = ""
        TmpValue = ""
        TmpValue2 = ""
        try:
            TmpValue = CfgFileDict[lineID][0]
        except:
            pass
        #TmpValue = TmpValue.strip() + "\n"
        #print TmpValue.decode('gbk')
        if TmpValue:
            #f.write(TmpValue)
            f.write(TmpValue.strip() + "\n")
        else:
            for item in CfgFileDict[lineID]:
                if item == "version":
                    f.write(item)
                    f.write("=")
                    f.write(CfgFileDict[lineID][item][0])
                    f.write("\n")
                else:
                    itemStr = "[" + item + "]"
                    f.write(itemStr)
                    f.write("\n")
                    if item == "insert_update_job" and insert_update_job_flag:
                        #CfgFileDict[lineID][item] = [[line[0], line[2]] for line in CtlConfDict['CTL.JOB_DEF'][1:]]
                        tmpValueStr = ""
                        try:
                            tmpValueStr = CfgFileDict[lineID][item]
                        except:
                            pass
                        if tmpValueStr:
                            #tmpValueStrList = CfgFileDict[lineID][item]
                            #CfgFileDict[lineID][item] = []
                            #for tmpValueStr in tmpValueStrList:
                            #    CfgFileDict[lineID][item].append(tmpValueStr)
                            CfgFileDict[lineID][item] = []
                            for tmpValueStr in [[line[0], line[2]] for line in CtlConfDict['CTL.JOB_DEF'][1:]]:
                                CfgFileDict[lineID][item].append(tmpValueStr)

                    if item == "insert_update_ds" and insert_update_ds_flag:
                        tmpValueStr = ""
                        try:
                            tmpValueStr = CfgFileDict[lineID][item]
                        except:
                            pass
                        if tmpValueStr:
                            CfgFileDict[lineID][item] = []
                            for tmpValueStr in [[line[0], line[2]] for line in CtlConfDict['CTL.TA_ETL_DS_DEF'][1:]]:
                                CfgFileDict[lineID][item].append(tmpValueStr)
                    for ID in CfgFileDict[lineID][item]:
                        ValueStr = ID[0]
                        #print str(ValueStr)
                        #ValueStr = str(ValueStr)
                        ValueStr = ValueStr.strip()
                        if ValueStr != "":
                            #print ValueStr
                            f.write(ValueStr)
                            f.write("\n")
                #f.write("\n")
        #pass
    f.close()

    Del = ','
    print "\n==============================Latest configuration info==============================\n"
    for CtlSheetName in CtlConfDict:
        print CtlSheetName + ":"
        #print CtlConfDict[CtlSheetName]
        lineID = 0
        for line in CtlConfDict[CtlSheetName]:
            lineID = lineID + 1
            linestr = ''
            Del = ','
            ColCnt = len(line)
            ColID = 0
            for Str in line:
                ColID = ColID + 1
                #print str
                Str = Str.decode('gbk')
                Str = Str.strip()
                    
                if linestr == '':
                    linestr = Str
                    #print linestr
                else:
                    #print str
                    #print linestr
                    linestr = linestr + Del + Str
                    #print linestr
            #print "\n"
            #linestr = linestr.strip()
            print linestr


    ##CfgFileDict = ReadCfgFile(CfgFile)
    ##ReqID = CfgFileDict['version']
    ##ExcelHandle = OpenExcel(ExcelFile)
    ##(SheetDict, CfgDataDict) = ReadExcel(ExcelHandle, CtlTableList, CfgFileDict)
    ret = WriteFile(ReqID, CtlConfDict, LatestCodeIDDict, LatestCodeIDFile, OutputPath)

    #print DDL

    #for Key in CfgFileDict:
    #    print Key, CfgFileDict[Key]

if __name__ == "__main__":
    Argc = len(sys.argv) - 1
    #print Argc
    if Argc < 2 or Argc > 5:
        print "Usage: ", sys.argv[0], "{<FullExcelFileName> <SheetName> | <ExcelCfg>} <CfgFile> [CtlExcelFile] [OutputPath]"
        sys.exit(1)
    searchCfgInfoFile = re.search(r'\.ctl$', str(sys.argv[1]), re.I|re.M)

    CfgInfoList = []
    if Argc in (3, 4, 5) and not searchCfgInfoFile:
        ExcelFile        = str(sys.argv[1])
        SheetName        = str(sys.argv[2])
        CfgFile          = str(sys.argv[3])
        CtlExcelFullName = ""
        try:
            CtlExcelFullName = str(sys.argv[4])
        except:
            CtlExcelFullName = "/home/hector/SVN_Working_Copy/ctl/最新配置表.xlsx"
            CtlExcelFullName = CtlExcelFullName.decode('gbk')

        try:
            OutputPath   = str(sys.argv[5])
        except:
            OutputPath   = os.path.dirname(CtlExcelFullName)
        #print OutputPath
        OutputPath  = os.path.abspath(OutputPath)
        CfgInfoList = [ExcelFile, SheetName]
    elif Argc in (2, 3, 4) and searchCfgInfoFile:
        CfgInfoFile      = str(sys.argv[1])
        CfgFile          = str(sys.argv[2])
        CtlExcelFullName = ""
        try:
            CtlExcelFullName = str(sys.argv[3])
        except:
            CtlExcelFullName = "/home/hector/SVN_Working_Copy/ctl/最新配置表.xlsx"
            CtlExcelFullName = CtlExcelFullName.decode('gbk')

        try:
            OutputPath   = str(sys.argv[4])
        except:
            OutputPath   = os.path.dirname(CtlExcelFullName)
        #print OutputPath
        OutputPath = os.path.abspath(OutputPath)
        if not os.path.isfile(CfgInfoFile):
            print "The config file is not exists! Please verify it!"
            sys.exit(1)

        f = OpenFile(CfgInfoFile)
        for line in f:
            ValueList = re.split(r'#', line)
            CfgInfoList.append(ValueList)

    Del = ","
    CtlTableList = '/home/hector/bin/CtlTableList.cfg'
    TemplateFile = '/home/hector/bin/CTL.Template.txt'
    LatestCodeIDFile = '/home/hector/bin/LatestCodeID.txt'
    CfgDataDict = {}
    
    ProgSchemaDict = {'TS'   : 'STAGE',
                      'TO'   : 'ODS'  ,
                      'TW'   : 'EDS'  ,
                      'TM'   : 'DM'   ,
                      'TR'   : 'REF'  ,
                      'TT'   : 'REF'  ,
                      'TP'   : 'RPT'  ,
                      'XML'  : 'XML'  }
    
    CodeCycleDict  = {'每月' : 'Mon' ,
                      '每周' : 'Day' ,
                      '每日' : 'Day' ,
                      '每天' : 'Day' }
    tmpCodeCycleDict = {}
    
    for key in CodeCycleDict:
        print key.decode('gbk'), CodeCycleDict[key]
        tmpCodeCycleDict[key.decode('gbk')] = CodeCycleDict[key]
    
    CodeCycleDict = tmpCodeCycleDict
    #print CodeCycleDict
    #sys.exit(1)
    CodeRefDict  = {'GmccMon:GmccMon' : '1',
                    'GmccDay:GmccDay' : '1',
                    'GmccMon:GmccDay' : '3'}
    TPRsProgDict = {'Day' : ['runstats.pl', '1'            ], 
                    'Mon' : ['runstats_mon.pl', '1'        ],
                    'None': ['runstats_nopartition.pl', '0']}

    main()
