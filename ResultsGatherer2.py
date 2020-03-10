# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 10:52:36 2019

@author: fredx
"""

import sys
import glob
import csv
import datetime

#Usage: python ResultsGatherer Path P1 P2

Path = ""
P1 = ""
P2 = ""
Files = []

def MixPercentages(Percentage1, Percentage2, W1, W2):
    Val1 = float(Percentage1) * float(W1) / 100.0
    Val2 = float(Percentage2) * float(W2) / 100.0   
    TotalVal = Val1 + Val2
    TotalW = float(W1) + float(W2)
    MixedPercentage = 100.0 * float(TotalVal) / float(TotalW)
    return MixedPercentage

def MixMeans(Mean1, Mean2, W1, W2):
    MixedMean = ((float(Mean1) * float(W1)) + (float(Mean2) * float(W2))) / (float(W1) + float(W2))
    return MixedMean

def GetData(Path, File):
    Barra = "\ "
    FileContent = []
    FileName = Path + Barra[0] + File
    
    with open(FileName) as csvfile:
        FileReader = csv.reader(csvfile, lineterminator = '\n')
        for Row in FileReader:
            NewRow = [x for x in Row]
            NewRow = str(NewRow[0])
            NewRow = NewRow.split(" ")[0]
            if NewRow in ["Experiment","PlayedGames","Wins","MeanScoreDifference","MeanBranchingFactor","TotalExpandedNodes","MeanPlayedMeeples","MeanFinalScore","MeanTurnsWithoutMeeples","MeanTurnTime","MeanExpandedNodes","MeanFarmMeeples","MeanCityMeeples","MeanRoadMeeples","MeanMonasteryMeeples","MeanFarmMeeplesPercentage","MeanCityMeeplesPercentage","MeanRoadMeeplesPercentage","MeanMonasteryMeeplesPercentage"]:
                FileContent.append(Row[0])
    return FileContent

def MixSameExperiment(Path, File, Attachment):
    Barra = "\ "
    FileContent = []
    FileName = Path + Barra[0] + File
    AttachmentName = Path + Barra[0] + Attachment
    MixedFile = []
    FileGames = 0.001
    AttachmentGames = 0.001
    HeadersList = ["Random","MCTS","Star25","MaxDepth","RolloutGames","Turn","Name"]
    
    with open(FileName) as csvfile:
        FileReader = csv.reader(csvfile, lineterminator = '\n')
        for Row in FileReader:
            FileContent.append(Row)
    #print(FileContent)
            
    with open(AttachmentName) as csvfile:
        FileReader = csv.reader(csvfile, lineterminator = '\n')
        for AttachmentRow in FileReader:
            #print("\nAttachmentRow",AttachmentRow)
            if AttachmentRow[0].split(" ")[0] in HeadersList:
                MixedFile.append(AttachmentRow[0])
            else:
                for FileRow in FileContent:
                    Match = False
                    FileRowName = FileRow[0].split(" ")[0]
                    AttachmentRowName = AttachmentRow[0].split(" ")[0]
                    if (FileRowName == AttachmentRowName):
                        if FileRowName == "ExperimentTime" or FileRowName == "Result" or FileRowName == "DrawnGames":
                            Match = True
                            Value = float(FileRow[0].split(" ")[1]) + float(AttachmentRow[0].split(" ")[1])
                        elif FileRowName == "PlayedGames":
                            Match = True
                            FileGames = float(FileRow[0].split(" ")[1])
                            AttachmentGames = float(AttachmentRow[0].split(" ")[1])
                            Value = str(int(FileGames + AttachmentGames))
                        elif FileRowName == "DrawnGamesPercentage":
                            Match = True
                            Value = MixPercentages(FileRow[0].split(" ")[1], AttachmentRow[0].split(" ")[1], FileGames, AttachmentGames)
                        elif FileRowName == "MeanBranchingFactor" or FileRowName == "MeanScoreDifference" or FileRowName == "StdDeviationScoreDifference" or FileRowName == "WinnerFinalScoreRelation":
                            Match = True
                            Value = MixMeans(FileRow[0].split(" ")[1], AttachmentRow[0].split(" ")[1], FileGames, AttachmentGames)
                        elif FileRowName == "Wins" or FileRowName == "TotalExpandedNodes":
                            Match = True
                            Lenght = len(FileRow[0].split(" "))
                            Value = ""
                            for i in range(Lenght - 1):
                                if not Value == "":
                                    Value += " "
                                Value = Value + str(float(FileRow[0].split(" ")[i + 1]) + float(AttachmentRow[0].split(" ")[i + 1]))
                        elif FileRowName == "StdDeviationTurnTime" or FileRowName == "StdDeviationFinalScore" or FileRowName == "MeanPlayedMeeples" or FileRowName == "MeanFinalScore" or FileRowName == "MeanTurnsWithoutMeeples"  or FileRowName == "MeanTurnTime" or FileRowName == "MeanExpandedNodes"  or FileRowName == "MeanExpandedCNodes"  or FileRowName == "MeanFarmMeeples"  or FileRowName == "MeanCityMeeples" or FileRowName == "MeanRoadMeeples" or FileRowName == "MeanMonasteryMeeples" or FileRowName in [str(x) for x in range(71)]:
                            Match = True
                            Lenght = len(FileRow[0].split(" "))
                            Value = ""
                            for i in range(Lenght - 1):
                                if not Value == "":
                                    Value += " "
                                Value = Value + str(MixMeans(FileRow[0].split(" ")[i + 1], AttachmentRow[0].split(" ")[i + 1], FileGames, AttachmentGames))
                        elif FileRowName == "VictoryPercentage"   or FileRowName == "MeanFarmMeeplesPercentage" or FileRowName == "MeanCityMeeplesPercentage" or FileRowName == "MeanRoadMeeplesPercentage" or FileRowName == "MeanMonasteryMeeplesPercentage":
                            Match = True
                            Lenght = len(FileRow[0].split(" "))
                            Value = ""
                            for i in range(Lenght - 1):
                                if not Value == "":
                                    Value += " "
                                Value = Value + str(MixPercentages(FileRow[0].split(" ")[i + 1], AttachmentRow[0].split(" ")[i + 1], FileGames, AttachmentGames))
                            
                            
                            
                        if Match:
                            Match = False
                            MixedRow = FileRowName + " " + str(Value)
                            MixedFile.append(MixedRow)
                            
    if File[0] == 'M' and File[1] == 'I' and File[2] == 'X':
        MixedFileName = Path + Barra[0] + File
        FinalName = File
    else:
        MixedFileName = Path + Barra[0] + "MIX" + File
        FinalName = "MIX" + File
    with open(MixedFileName, 'w') as csvfile:
        FileW = csv.writer(csvfile, lineterminator = '\n')
        for iRow in MixedFile:
            FileW.writerow([iRow])
    
            
    #print("\nMixedFile\n",MixedFile)                        
    return FinalName


if __name__ == '__main__':
    if len(sys.argv) > 1:
        Path = str(sys.argv[1])
    if len(sys.argv) > 2:
        P1 = str(sys.argv[2])
    if len(sys.argv) > 3:
        P2 = str(sys.argv[3])
    
    Now = datetime.datetime.now()
    Date = str(Now.hour) + "h" + str(Now.minute) + " " + str(Now.day) + "-" + str(Now.month) + "-" + str(Now.year)
    SearchString = Path + "/*" + P1 + "*-*" + P2 + "*-*-*-*-*.csv"
    RelativePathFiles = glob.glob(SearchString)
    ParamsList = ["Random","MCTS","Star25","MaxDepth","RolloutGames"]
    HeadersList = ["Turn","Name"]
    
    print("SearchString", SearchString)
    #print(RelativePathFiles)
    
    for iFileName in RelativePathFiles:
        Files.append(iFileName.split("\\")[-1])
    print("\nFiles",Files)
    
    ExperimentFiles = [x for x in Files if x.split("-")[2] == "0"]
    AddendumFiles = [x for x in Files if not x.split("-")[2] == "0"]
    
    print("\nExperimentFiles",ExperimentFiles)
    print("\nAddendumFiles",AddendumFiles)
    
    NewExperimentFiles = [x for x in ExperimentFiles]
    for iEFile in ExperimentFiles:
        AttachedFiles = [x for x in AddendumFiles if iEFile.split("-")[0] == x.split("-")[0] and iEFile.split("-")[1] == x.split("-")[1]]
        print("\niEFile",iEFile)
        print("AttachedFiles",AttachedFiles)
        for iAttachedFile in AttachedFiles:
            OldFile = iEFile + ""
            iEFile = MixSameExperiment(Path, iEFile, iAttachedFile)
            if OldFile in NewExperimentFiles:
                NewExperimentFiles.remove(OldFile)
            if iEFile not in NewExperimentFiles:
                NewExperimentFiles.append(iEFile)
            
    
    ExtractedData = []
    print("\nNewExperimentFiles",NewExperimentFiles)
    for iFile in NewExperimentFiles:
        ExtractedData.append(GetData(Path, iFile))
    #print("\nExtractedData",ExtractedData)
    CombinedData = []
    AllRowNames = []
    FileLenghts = [len(x) for x in ExtractedData]
    #print(FileLenghts)
    MaxLenght = max(FileLenghts)
    for iFileOutputIndex in range(len(ExtractedData)):
        #print("iFileOutputIndex",iFileOutputIndex)
        for iRowIndex in range(MaxLenght):
            #print("iRowIndex",iRowIndex)
            if len(ExtractedData[iFileOutputIndex]) > iRowIndex:
                if ExtractedData[iFileOutputIndex][iRowIndex].split(" ")[0] in ParamsList:
                    CombinedData.append(ExtractedData[iFileOutputIndex][iRowIndex])
                    
    #print("\nExtractedData:\n",ExtractedData)
    Row = ExtractedData[0]
    NewString = "Headers   "
    for iParam in Row:
        ParamHeader = iParam.split(" ")[0]
        Params = iParam.split(" ")[1:]
        LineEnd = ""
        for i in range(len(Params)):
            LineEnd += " "
        NewString += str(ParamHeader) + LineEnd
    CombinedData.append(NewString)
            
            
    for iRowIndex in range(len(ExtractedData)):
        iRow = ExtractedData[iRowIndex]
    #for iRow in ExtractedData:
        NewLine = str(NewExperimentFiles[iRowIndex]) + " "
        for iParam in iRow:
            ParamValues = iParam.split(" ")[1:]
            NewString = ""
            for Param in ParamValues:
                NewString += str(Param) + " "
            NewLine += str(NewString)
        CombinedData.append(NewLine)
        
    
    
    
    
    """
    ExperimentsString = "Experiment "
    for Exp in NewExperimentFiles:
        ExperimentsString += str(Exp).replace(" ","") + " "
        
    for iRowIndex in range(MaxLenght):
        NewLine = ""
        LineHeader = True
        ActualLineHeader = ""
        for iFileOutputIndex in range(len(ExtractedData)):
            if len(ExtractedData[iFileOutputIndex]) > iRowIndex:
                if LineHeader:
                    LineHeader = False
                    NewLine += str(ExtractedData[iFileOutputIndex][iRowIndex])
                    ActualLineHeader += str(ExtractedData[iFileOutputIndex][iRowIndex].split(" ")[0])
                else:
                    for iiRowIndex in range(MaxLenght):
                        if len(ExtractedData[iFileOutputIndex]) > iiRowIndex:                        
                            if str(ExtractedData[iFileOutputIndex][iiRowIndex].split(" ")[0]) == ActualLineHeader:
                                if ActualLineHeader in [str(x) for x in range(36,71)]:
                                    Temp = ExtractedData[iFileOutputIndex][iiRowIndex].split(" ")[1:]
                                    Temp2 = "      "
                                    for item in Temp:
                                        Temp2 += str(item) + " "
                                    NewLine += " " + Temp2[:-1]
                                else:
                                    Temp = ExtractedData[iFileOutputIndex][iiRowIndex].split(" ")[1:]
                                    Temp2 = ""
                                    for item in Temp:
                                        Temp2 += str(item) + " "
                                    NewLine += " " + Temp2[:-1]
        CombinedData.append(NewLine)
    #print(CombinedData)
    """
    
    
    #"""
    ResultName = "GatheredResults " + P1 + "-" + P2 + Date + ".csv"
    with open(ResultName, 'w') as csvfile:
            FileW = csv.writer(csvfile, lineterminator = '\n')
            for iRow in CombinedData:
                FileW.writerow([iRow])
    #"""
