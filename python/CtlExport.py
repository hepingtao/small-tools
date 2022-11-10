#!/usr/bin/python
# -*- coding:utf-8 -*-

import xdrlib, sys
import xlrd
import datetime
import os
#from datetime import timedelta
import re

reload(sys)
sys.setdefaultencoding("utf-8")

Del = ","
CtlTableList = '/home/hector/bin/CtlTableList.cfg'
CfgDataDict = {}

##def ReadCfgFileCfgInfo(CfgFile):
##    BaseCfgFileName = os.path.splitext(os.path.basename(CfgFile))[0]
##    CfgFileDict    = {}
##    CfgFileCfgDict = {}
##    tmpCfgFileCfgDict = {}
##    Key   = ""
##    Value = ""
##    f = OpenFile(CfgFile)
##    lineID = 0
##    for line in f:
##        lineID = lineID + 1
##
##        searchObj = re.search(r'^(version)=(.*)$', line, re.I|re.M)
##        if searchObj:
##            Key   = searchObj.group(1)
##            Value = searchObj.group(2)
##            if BaseCfgFileName != Value:
##                print "The version ID of Cfg info is wrong, not as same as cfg filename, please modify it first!"
##                sys.exit(1)
##            CfgFileCfgDict[Key] = Value
##            #Key = ""
##
##        searchKeyObj = re.search(r'^\[(insert_update_job|del_job|insert_update_ds|del_ds)\].*$', line, re.I|re.M)
##        searchValueObj = re.search(r'^[A-Za-z0-9_\., ]+ *$', line, re.I|re.M)
##        if searchKeyObj:
##            Key = searchKeyObj.group(1)
##            #print Key
##            CfgFileCfgDict[Key] = []
##            tmpCfgFileCfgDict = {}
##            tmpCfgFileCfgDict[Key] = []
##            CfgFileDict[lineID] = tmpCfgFileCfgDict
##        elif searchValueObj:
##            ValueList = re.split(',| +', line)
##            #print TmpValueList
##            CfgFileCfgDict[Key].append(ValueList)
##            tmpCfgFileCfgDict[Key].append(ValueList)
##            #print tmpCfgFileCfgDict
##        else:
##            CfgFileDict[lineID] = line
##            continue
##
##    return CfgFileDict, CfgFileCfgDict
    
    
def ReadCfgFile(CfgFile):
    CfgFileDict = {'insert_update_job': '',
                   'del_job'          : '',
                   'insert_update_ds' : '',
                   'del_ds'           : '',
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
    try:
        data = xlrd.open_workbook(ExcelFile)
        return data
    except Exception,e:
        print str(e)


def OpenFile(FileName):
    try:
        f = open(FileName,'r')
        return f
    except Exception,e:
        print str(e)

def GetDsFileNameDict():
    #FullCTLFileName = OutputPath + "/" + "CTL.TA_ETL_DS_DEF.txt"
    #DsIDFileNameDict = {}
    DsFileNameDict = {}
    DsIDExistFlag = 0
    SheetName  = "CTL.TA_ETL_DS_DEF"
    KeyColList = [1]
    #(lineIDDict, CTLDataDict) = ReadCTLData(FullCTLFileName, KeyColList)
    ExcelHandle = OpenExcel(ExcelFile)
    Sheet = ExcelHandle.sheet_by_name(SheetName)
    #print type(Sheet)
    #sys.exit(1)
    nrows = Sheet.nrows
    for RowID in range(0, nrows):
        #sRowID = str(sRowID)
        #print rownum
        rowvaluelist = Sheet.row_values(RowID)
        #rowvaluelist = [re.sub(r'\.0.*$', "", str(CellValue)) for CellValue in rowvaluelist]
        #print CellValue
        #print type(CellValue)
        #KeyStr = ""
        ##for ColID in range(0, KeyCnt):
        #for ColID in KeyColList:
        #    ColID = int(ColID) - 1
        #    Cell = rowvaluelist[ColID]
        #    if KeyStr:
        #        KeyStr = KeyStr + Del + Cell
        #    else:
        #        KeyStr = Cell

        #DsIDFileNameDict[KeyStr] = rowvaluelist
        #CellValue = rowvaluelist[0]
        #CellValue = re.sub(r'\.0.*$', "", str(CellValue))
        DsID = rowvaluelist[0]
        DsFileName = rowvaluelist[6]
        DsID = re.sub(r'\.0.*$', "", str(DsID))
        DsFileName = DsFileName.encode('gbk')
        DsFileName = re.sub(r'["\(\)$]', '', DsFileName)
        #if CellValue == Ds_ID:
        #    DsFileName = rowvaluelist[6]
        #    DsFileName = DsFileName.encode('gbk')
        #    DsIDExistFlag = 1
        if DsFileName:
            DsFileNameDict[DsID] = DsFileName
    
    #if DsIDExistFlag == 1:
    #    #print Ds_ID + ": " + DsFileName
    #    pass
    #else:
    #    print "The DsID " + Ds_ID + " is not exist in " + SheetName + "!"
    #    sys.exit(1)

    return DsFileNameDict

def GetRefJobIDDict():
    RefJobIDDict = {}
    JobIDExistFlag = 0
    SheetName = "CTL.JOB_REF"
    ExcelHandle = OpenExcel(ExcelFile)
    Sheet = ExcelHandle.sheet_by_name(SheetName)
    nrows = Sheet.nrows
    for RowID in range(0, nrows):
        #sRowID = str(sRowID)
        #print rownum
        rowvaluelist = Sheet.row_values(RowID)
        JobID = rowvaluelist[0]
        RefJobID = rowvaluelist[1]
        JobID = re.sub(r'\.0.*$', "", str(JobID))
        RefJobID = re.sub(r'\.0.*$', "", str(RefJobID))
        TmpValue = ""
        try:
            TmpValue = RefJobIDDict[JobID]
        except:
            RefJobIDDict[JobID] = []
        #if CellValue == JobID:
        #    RefJobID = rowvaluelist[1]
        #    RefJobID = re.sub(r'\.0.*$', "", str(RefJobID))
        #    RefJobIDList.append(RefJobID)
        #    JobIDExistFlag = 1
        if RefJobID:
            RefJobIDDict[JobID].append(RefJobID)
    
    #if JobIDExistFlag == 1:
    #    #print Ds_ID + ": " + DsFileName
    #    pass
    #else:
    #    print "The JobID " + JobID + " is not exist in " + SheetName + "!"
    #    sys.exit(1)
    #print RefJobIDDict['12105008']
    #sys.exit(1)

    return RefJobIDDict

def GetTabStr(SheetName, table, Cols, IDListDict, KeyColList):
    nrows = table.nrows  #rows
    ncols = table.ncols  #cols
    #print nrows, ncols
    #print OutputPath, SheetName
    #print IDListDict
    RefJobIDDict = {}
    DsFileNameDict = {}
    if SheetName == "CTL.JOB_PARAM_DEF":
        RefJobIDDict = GetRefJobIDDict()
        DsFileNameDict = GetDsFileNameDict()

    TabStr = {}
    FullCTLFileName = ""
    lineIDDict  = {}
    CTLDataDict = {}
    for IDType in IDListDict:
        DeleteFlag = ""
        IDList = IDListDict[IDType]
        #print IDType
        #print IDList
        searchDelObj = re.search(r'^del_', IDType, re.I|re.M)
        if IDList and searchDelObj:
            FullCTLFileName = OutputPath + "/" + SheetName + ".txt"
            print FullCTLFileName
            (lineIDDict, CTLDataDict) = ReadCTLData(FullCTLFileName, KeyColList)
        for ID in IDList:
            IDExistFlag = 0
            #print CellValue
            ID = ID.strip()
            #print ID
            #print type(ID)
            if searchDelObj:
                txtKeyStrList = [lineIDDict[lineID] for lineID in lineIDDict]
                txtIDList =[KeyList[0] for KeyList in [KeyStr.split(',') for KeyStr in txtKeyStrList]]
                if ID in txtIDList:
                    DelKeyStrList = [KeyStr for KeyStr in txtKeyStrList if KeyStr.split(',')[0] == ID]
                    for KeyStr in DelKeyStrList:
                        CTLDataDict[KeyStr] = ""
                    DeleteFlag = "1"
                else:
                    print "There isn't dsid or jobid " + ID + " in CTL txt file " + FullCTLFileName
                    DeleteFlag = ""

            #iID = int(ID)
            for rownum in range(0,nrows):
                sRowID = str(rownum + 1)
                #print rownum
                rowvaluelist = table.row_values(rownum)
                #rowvaluelist = table.row(rownum)
                CellValue = rowvaluelist[0]
                #CellValue = str(int(CellValue))
                CellValue = re.sub(r'\.0.*$', "", str(CellValue))
                #print CellValue
                #print type(CellValue)
                #if CellValue == iID:
                if CellValue == ID:
                #if CellValue is ID:
                    IDExistFlag = 1
                    if searchDelObj:
                        print "Please delete the dsid or jobid " + ID + " at line " + sRowID + " in Sheet " + SheetName + " first!"
                        sys.exit(1)
                        #break
                    #print type(CellValue)
                    #print CellValue
                    #print ID
                    Del = ','
                    #ValueStr = Del.join(rowvaluelist)
                    ValueStr = ""
                    ColID = 0
                    for Cell in rowvaluelist:
                        ColID = ColID + 1
                        if ColID <= Cols:
                            Cell = str(Cell)
                            Cell = re.sub(r'\.0.*$', "", Cell)
                            #print Cell
                            if ValueStr:
                                ValueStr = ValueStr + Del + Cell
                            else:
                                ValueStr = Cell
                    ValueStr = ValueStr.encode('gbk')

                    if SheetName == 'CTL.JOB_PARAM_DEF' and IDType == 'insert_update_job':
                        ParamDef  = rowvaluelist[6]
                        if ParamDef: ParamDef  = str(ParamDef)
                        ParamDef = ParamDef.encode('gbk')
                        JobID = ID
                        Ds_ID = ""
                        PassJobID = ""
                        searchID_DsObj = re.search(r'^11([0-9]{4})[0-9]{2}$', JobID, re.I|re.M)
                        #searchValue_PassJobIDObj = re.search(r'\$([0-9]{8})\.', ParamDef, re.I|re.M)
                        searchValue_PassJobIDObj = re.findall(r'\$([0-9]{8})\.', ParamDef, re.I|re.M)
                        if searchValue_PassJobIDObj:
                            #PassJobID = searchValue_PassJobIDObj.group(1)
                            PassJobIDList = searchValue_PassJobIDObj
                            Ref_JobIDList = RefJobIDDict[JobID]
                            #print Ref_JobIDList
                            for PassJobID in PassJobIDList:
                                if PassJobID not in Ref_JobIDList:
                                    sRefJobID = ' '.join(sorted(Ref_JobIDList))
                                    print JobID + ": " + sRefJobID
                                    print "Line " + sRowID + ": " +ValueStr
                                    print "the job ID " + PassJobID + " passing the parameter is not in refjob ID list, please verify!"
                                    sys.exit(1)
                            
                        if searchID_DsObj:
                            Ds_ID = searchID_DsObj.group(1)
                            searchValue_SubFNObj = re.search(r'\$11([0-9]{4})[0-9]{2}\.objectfile\[([0-9]{1,}),([0-9]{1,})\]', ParamDef, re.I|re.M)
                            if searchValue_SubFNObj:
                                Pre_Ds_ID = searchValue_SubFNObj.group(1)
                                StartPos  = searchValue_SubFNObj.group(2)
                                EndPos    = searchValue_SubFNObj.group(3)
                                #EndPos    = int(EndPos)
                                if Ds_ID != Pre_Ds_ID:
                                    print "the Ds_ID of the jobID that pass parameters is wrong!"
                                    sys.exit(1)
                                Ds_ID = re.sub(r'^0+', '', Ds_ID)
                                Ds_FileName = DsFileNameDict[Ds_ID]
                                Ds_BaseFileName = Ds_FileName
                                Ds_FNLen = 0
                                searchDsFN_CObj = re.search(r'(\.Z)|(.gz)|(.zip)$', Ds_FileName, re.I|re.M)
                                if searchDsFN_CObj:
                                    Ds_BaseFileName = os.path.splitext(os.path.basename(Ds_FileName))[0]
                                Ds_FNLen = len(Ds_BaseFileName)
                                Ds_FNLen = str(Ds_FNLen)

                                if EndPos != Ds_FNLen:
                                    print Ds_ID + ": " + Ds_FileName
                                    print "Line " + sRowID + ": " +ValueStr
                                    print "The base file name is " + Ds_BaseFileName + ", its length is " + Ds_FNLen + ", so the end pos " + EndPos + " is wrong!"
                                    sys.exit(1)

                    #print ValueStr
                    KeyStr = ""
                    #for ColID in range(0, KeyCnt):
                    for ColID in KeyColList:
                        ColID = int(ColID) - 1
                        Cell = str(rowvaluelist[ColID])
                        Cell = re.sub(r'\.0.*$', "", Cell)
                        if KeyStr:
                            KeyStr = KeyStr + Del + Cell
                        else:
                            KeyStr = Cell

                    TabStr[KeyStr] = ValueStr

            if IDExistFlag == 0 and SheetName in ('CTL.TA_ETL_DS_DEF', 'CTL.JOB_DEF'):
                print "No CTL data of " + ID + " in sheet " + SheetName + " of " + ExcelFile
                print "Please verify it!"
                #sys.exit(1)

        if DeleteFlag:
            try:
                os.remove(FullCTLFileName)
            except OSError:
                pass
            UpdateCtl(FullCTLFileName, lineIDDict, CTLDataDict)
            print "The dsid or jobid " + ID + " in CTL txt file " + FullCTLFileName + " have been deleted!"

    #sys.exit(1)
    return TabStr


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

def ReadExcel(ExcelHandle, CtlTableList, CfgFileDict):
    CfgDataDict = {}
    #SheetIDList = []
    SheetNameList = []
    IDList = {}
    SheetDict = GetSheetInfo(CtlTableList)

    for SheetID in sorted(SheetDict):
        SheetName = SheetDict[SheetID][0]
        Cols      = int(SheetDict[SheetID][1])
        SheetType = SheetDict[SheetID][2]
        KeyCols   = SheetDict[SheetID][3]
        KeyCols   = re.sub(r'\[(.*)\]', r'\1', KeyCols)
        KeyColList = KeyCols.split('#')
        print SheetName
        IDListDict = {}
        #searchObj = re.search(r'^CTL\.(TA_ETL_DS_DEF|TA_ETL_DS_HOST|TA_ETL_DS_FIELDS|DS_CNT_DEF|TA_ETL_LOAD_CTRL|DATA_CLEAR_RULES|TA_ETL_CLEAN_RULE|TA_ETL_QUALITY_CONTROL) *$', SheetName, re.M|re.I)
        #if searchObj:
        if SheetType == '1':
            IDListDict['insert_update_ds'] = CfgFileDict['insert_update_ds']
            IDListDict['del_ds'] = CfgFileDict['del_ds']
        
        #searchObj = re.search(r'^CTL\.(JOB_DEF|JOB_PARAM_DEF|JOB_REF|JOB_TIME_REF|JOB_OPR_OBJ|JOB_LEVEL_CTRL|JOB_LIMIT) *$', SheetName, re.M|re.I)
        #if searchObj:
        if SheetType == '2':
            IDListDict['insert_update_job'] = CfgFileDict['insert_update_job']
            IDListDict['del_job'] = CfgFileDict['del_job']
        
        #searchObj = re.search(r'^CTL\.(TA_ETL_DS_DEF|TA_ETL_LOAD_CTRL|JOB_DEF) *$', SheetName, re.M|re.I)
        #if searchObj:
        #    KeyCnt = 1
        #
        #searchObj = re.search(r'^CTL\.(TA_ETL_DS_HOST|TA_ETL_DS_FIELDS|DS_CNT_DEF|DATA_CLEAR_RULES|JOB_OPR_OBJ|JOB_LIMIT) *$', SheetName, re.M|re.I)
        #if searchObj:
        #    KeyCnt = 2

        #searchObj = re.search(r'^CTL\.(TA_ETL_CLEAN_RULE|JOB_LEVEL_CTRL) *$', SheetName, re.M|re.I)
        #if searchObj:
        #    KeyCnt = 3

        #searchObj = re.search(r'^CTL\.(TA_ETL_QUALITY_CONTROL|JOB_PARAM_DEF|JOB_REF|JOB_TIME_REF) *$', SheetName, re.M|re.I)
        #if searchObj:
        #    KeyCnt = 4

        #print KeyCnt
        table = ExcelHandle.sheet_by_name(SheetName)
        tmpCfgDataDict = GetTabStr(SheetName, table, Cols, IDListDict, KeyColList)
        CfgDataDict[SheetName] = tmpCfgDataDict

    #print CfgDataDict
    #sys.exit(1)

    return SheetDict, CfgDataDict


def WriteFile(ReqID, SheetDict, CfgDataDict):
    AppendFlag = "0"
    UpdateFlag = "0"
    lineIDDict = {}
    CTLDataDict = {}
    tmplineIDDict = {}
    tmpCTLDataDict = {}
    AppendlineIDDict  = {}
    AppendCTLDataDict = {}
    OutputFile = OutputPath + "/" + ReqID + ".OUT"
    #DDL = DDL.encode('cp936')
    print OutputFile
    #if os.path.exists(OutputFile):
    #    os.unlink(OutputFile)
    try:
        os.remove(OutputFile)
    except OSError:
        pass
    f = open(OutputFile,"a")
    for SheetID in sorted(SheetDict):
        AppendlineIDDict  = {}
        AppendCTLDataDict = {}
        AppendFlag = "0"
        UpdateFlag = "0"
        ReplaceFlag = "0"
        SheetName = SheetDict[SheetID][0]
        print "=================" + SheetName + "================="
        CTLFileName = SheetName + ".txt"
        FullCTLFileName = OutputPath + "/" + CTLFileName
        KeyCols   = SheetDict[SheetID][3]
        KeyCols   = re.sub(r'\[(.*)\]', r'\1', KeyCols)
        KeyColList = KeyCols.split('#')
        KeyStrDict = CfgDataDict[SheetName]
        KeyStrList = KeyStrDict.keys()
        if KeyStrDict:
            f.write(CTLFileName)
            f.write('\n')
            (lineIDDict, CTLDataDict) = ReadCTLData(FullCTLFileName, KeyColList)
            TailLineID = 1
            try:
                TailLineID = max(lineIDDict.keys())
            except:
                pass
            #txtKeyStrList = lineIDDict.values()
            txtCTLKeyStrList = CTLDataDict.keys()
            #sys.exit(1)

            IDDict = {}
            IDList = [KeyStr.split(',')[0] for KeyStr in KeyStrList]
            for ID in IDList:
                IDDict[ID] = 1

            DelLineID = 0
            for ID in IDDict:
                #txtCTLKeyList = []
                try:
                    #txtCTLKeyList = [txtKeyStr for txtKeyStr in txtCTLKeyStrList if txtKeyStr.split(',')[0] == ID]
                    txtlineIDList = [lineID for lineID in lineIDDict if lineIDDict[lineID].split(',')[0] == ID]
                except:
                    pass
                #print txtlineIDList
                #for txtCTLKey in txtCTLKeyList:
                for lineID in txtlineIDList:
                    #print CTLDataDict[txtCTLKey]
                    txtCTLKey = lineIDDict[lineID]
                    if txtCTLKey not in KeyStrList:
                        print "delete====================="
                        print CTLDataDict[txtCTLKey]
                        #CTLDataDict[txtCTLKey] = ""
                        #txtCTLKeyList.remove(txtCTLKey)
                        #txtlineIDList.remove(lineID)
                        del lineIDDict[lineID]
                        del CTLDataDict[txtCTLKey]
                        DelLineID = lineID
                        UpdateFlag = "1"
                        ReplaceFlag = "1"
                        #print "Do you fuck?"

            #for K in txtKeyStrList:
            #    #print K
            #    searchObj = re.search(r'^12303256', K, re.I|re.M)
            #    if searchObj:
            #        print K
            #        print CTLDataDict[K] 
            #sys.exit(1)
            lineID = 0
            #for KeyStr in sorted(KeyStrDict):
            #for KeyStr in sorted(KeyStrDict, key=lambda x:int(x.split(',')[1])):
            if SheetName == 'CTL.JOB_PARAM_DEF':
                KeyStrSortList = sorted(KeyStrList, key=lambda x: (x.split(',')[0], int(x.split(',')[1])))
            else:
                KeyStrSortList = sorted(KeyStrList)
            for KeyStr in KeyStrSortList:
                #KeyStr = KeyStr.encode('gbk')
                #KeyStr = KeyStr.strip()
                ID = KeyStr.split(',')[0]
                lineID = lineID + 1
                #print KeyStr
                #ValueStr = CfgDataDict[SheetName][KeyStr]
                ValueStr = KeyStrDict[KeyStr]
                #ValueStr = ValueStr.encode('gbk')
                ValueStr = ValueStr.rstrip('\r')
                #print ValueStr
                if ValueStr:
                   f.write(ValueStr)
                   f.write('\n')

                (tmplineIDDict, tmpCTLDataDict) = ReadCTLData(FullCTLFileName, KeyColList)
                txtKeyStrList = tmpCTLDataDict.keys()
                
                TmpValue = ""
                if KeyStr in txtKeyStrList:
                #if KeyStr in CTLDataDict.keys():
                    #print KeyStr
                    #KeyStr = KeyStr.encode('utf8')
                    TmpValue = tmpCTLDataDict[KeyStr]
                    #print TmpValue
                
                #for CTLKeyStr in CTLDataDict:
                #    #CTLKeyStr = CTLKeyStr.encode('gbk')
                #    CTLKeyStr = CTLKeyStr.strip()
                #    if CTLKeyStr == KeyStr:
                #        TmpValue = CTLDataDict[CTLKeyStr]
                #for txtKeyStr in CTLDataDict.keys():
                #    #searchObj = re.search(r'^12303256', txtKeyStr, re.I|re.M)
                #    #if searchObj:
                #    #    print txtKeyStr
                #    #    print CTLDataDict[txtKeyStr]
                #    if txtKeyStr == KeyStr:
                #        TmpValue = CTLDataDict[txtKeyStr]
                #print "========================================"
                #print TmpValue
                #print "========================================"
                if TmpValue:
                    #print "exists================"
                    #print KeyStr
                    #print TmpValue
                    #print ValueStr
                    if ValueStr != TmpValue:
                        print "different====================="
                        print TmpValue.decode('gbk')
                        print ValueStr.decode('gbk')
                        CTLDataDict[KeyStr] = ValueStr
                        UpdateFlag = "1"
                        #fCTL = open(FullCTLFileName,"r+")
                        #print "UpdateCtl(FullCTLFileName, lineIDDict, CTLDataDict, KeyStr, ValueStr)"
                        #print CTLDataDict[KeyStr]
                        #print ValueStr
                else:
                    if KeyStr:
                        #if ReplaceFlag == "1":
                        print "not exists====================="
                        print KeyStr.decode('gbk')
                        print ValueStr.decode('gbk')
                        #AppendlineIDDict[lineID]  = KeyStr
                        #AppendCTLDataDict[KeyStr] = ValueStr
                        #lineIDDict = AppendlineIDDict
                        #CTLDataDict = AppendCTLDataDict
                        #lineIDDict = AppendlineIDDict
                        FirstKeyStr = ""
                        try:
                            #FirstKeyStr = [txtKeyStr for txtKeyStr in txtKeyStrList if txtKeyStr.split(',')[0] == ID][0]
                            FirstKeyStr = [lineIDDict[txtlineID] for txtlineID in sorted(lineIDDict) if lineIDDict[txtlineID].split(',')[0] == ID][0]
                        except:
                            pass
                            
                        LastKeyStr = ""
                        Ds_ID = ""
                        searchID_DsObj = re.search(r'^11([0-9]{4})[0-9]{2}$', ID, re.I|re.M)
                        if searchID_DsObj:
                            Ds_ID = searchID_DsObj.group(1)
                            try:
                                LastKeyStr = [lineIDDict[txtlineID] for txtlineID in sorted(lineIDDict) if lineIDDict[txtlineID].split(',')[0][2:6] == Ds_ID][-1]
                            except:
                                pass
                        if FirstKeyStr:
                            CTLDataDict[FirstKeyStr] = CTLDataDict[FirstKeyStr] + "\n" + ValueStr
                        elif LastKeyStr:
                            CTLDataDict[LastKeyStr]  = CTLDataDict[LastKeyStr]  + "\n" + ValueStr
                        else:
                            if DelLineID > 0:
                                #DelLineID = DelLineID + 1
                                #TmpValue = ""
                                #try:
                                #    TmpValue = lineIDDict[DelLineID]
                                #except:
                                #    pass
                                #if TmpValue:
                                #    print "replaced====================="
                                #    print TmpValue
                                    
                                #print DelLineID
                                #lineIDDict[DelLineID] = KeyStr
                                lineIDDict[DelLineID] = DelLineID
                                TmpValue = ""
                                try:
                                    TmpValue = CTLDataDict[DelLineID]
                                except:
                                    pass
                                if TmpValue:
                                    CTLDataDict[DelLineID] = CTLDataDict[DelLineID] + "\n" + ValueStr
                                else:
                                    CTLDataDict[DelLineID] = ValueStr
                            else:
                                TailLineID = TailLineID + 1
                                lineIDDict[TailLineID] = KeyStr
                                CTLDataDict[KeyStr] = ValueStr
                                
                        UpdateFlag = "1"
                        #sys.exit(1)

            f.write('\n')
            #UpdateWishFlag = ""
            if UpdateFlag == "1":
                #UpdateWishFlag = raw_input("Update it now? ")
                #searchUWFObj = re.search(r'^y(es)?$', UpdateWishFlag, re.I|re.M)
                #if searchUWFObj:
                    #pass
                    #if UpdateFlag == "1":
                    #    try:
                    #        os.remove(FullCTLFileName)
                    #    except OSError:
                    #        pass
                    #print "Updating ..."
                    #UpdateCtl(FullCTLFileName, lineIDDict, CTLDataDict)
                    #print "Updated, you should check the result bascally!"
                print "Updating ..."
                UpdateCtl(FullCTLFileName, lineIDDict, CTLDataDict)
                print "Updated, you should check the result bascally now!"
                    
    f.close()


def UpdateCtl(FullCTLFileName, lineIDDict, CTLDataDict):
    try:
        os.remove(FullCTLFileName)
    except OSError:
        pass
    f = open(FullCTLFileName, 'a')
    #KeyList = [for lineID in sorted(lineIDDict)]
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

        #TmpValue = ""
        #try:
        #    TmpValue = CTLDataDict[KeyStr]
        #except:
        #    pass

        #if TmpValue:
        #    CTLDataDict[KeyStr] = line + "\n" + TmpValue
        #else:
        #    CTLDataDict[KeyStr] = line

    f.close()
    #sys.exit(1)

    return lineIDDict, CTLDataDict


def main():

    CfgFileDict = {}
    #insert_update_job
    #del_job
    #insert_update_ds
    #del_ds

    CfgFileDict = ReadCfgFile(CfgFile)
    ReqID = CfgFileDict['version']
    ExcelHandle = OpenExcel(ExcelFile)
    (SheetDict, CfgDataDict) = ReadExcel(ExcelHandle, CtlTableList, CfgFileDict)
    ret = WriteFile(ReqID, SheetDict, CfgDataDict)

    #print DDL

    #for Key in CfgFileDict:
    #    print Key, CfgFileDict[Key]

if __name__ == "__main__":
    #print 'Argumnet List:',str(sys.argv)
    if len(sys.argv) < 2:
        print "Usage: ", sys.argv[0], "<CfgFile> [FullExcelFileName] [OutputPath]"
        sys.exit(1)

    CfgFile    = str(sys.argv[1])
    ExcelFile  = ""
    try:
        ExcelFile  = str(sys.argv[2])
    except:
        ExcelFile  = "/home/hector/SVN_Working_Copy/ctl/最新配置表.xlsx"
        #ExcelFile  = ExcelFile.decode('gbk')
        #CtlExcelFullName = CtlExcelFullName.decode('gbk')

    OutputPath = ""
    try:
        OutputPath = str(sys.argv[3])
    except:
        OutputPath = os.path.dirname(ExcelFile)
    OutputPath  = os.path.abspath(OutputPath)
    #print OutputPath

    #searchObj = re.search(r'^(\D+[-0-9]*)(.*)$', CfgFile, re.M|re.I)
    #print searchObj.group()
    #print searchObj.group(1)
    #print searchObj.group(2)
    #sys.exit(1)

    #print CfgFile

    main()
