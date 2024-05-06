def FTtoM(value):
    return value*0.3048

def MtoFT(value):
    return value/0.3048

def MItoM(value):
    return value*1609.34

def MtoMI(value):
    return value/1609.34

def HPtoW(value):
    return value*745.7
    
def MPHtoMS(value):
    return MItoM(value)/3600.0

def MStoMPH(value):
    return MtoMI(value)*3600.0

def KGM3toSPFT3(value):
    return value*0.00194032

def NtoLBSF(value):
    return value*0.224809

def WtoSLUGSFT2S_3(value):
    return value / 1.35581795