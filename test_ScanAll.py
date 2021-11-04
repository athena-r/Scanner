import pytest
from ScanAll import Scanner
#Checking the functions in the ScannerClass file to make sure the 
#data types returned are correct and correct exceptions are caught

@pytest.fixture(scope='module')
def goodScan():
    goodScan=Scanner('testfiles/test4')
    return goodScan
@pytest.fixture(scope='module')
def badScan():
    badScan=Scanner('nonexistentfile','fakedict')
    #This file does not exist, so they should raise exceptions
    return badScan

def test_getData(goodScan,badScan):
    assert type(goodScan.getData())==bytes
    assert len(goodScan.getData())>0

    noCheckFile=Scanner('')
    with pytest.raises(FileNotFoundError):
        noCheckFile.getData()
    with pytest.raises(FileNotFoundError):
        badScan.getData()

def test_getDict(goodScan,badScan):
    assert type(goodScan.getDict())==list
    assert len(goodScan.getDict())>0

    noDict=Scanner('testfiles/test4','')     
    with pytest.raises(FileNotFoundError):
        noDict.getDict()

    with pytest.raises(FileNotFoundError):
        badScan.getDict()

def test_checkAll(goodScan,badScan):
    assert type(goodScan.checkAll())==int
    assert goodScan.checkAll()>0

def test_scanner(goodScan,badScan):
    with pytest.raises(TypeError):
        noInput=Scanner()
        noInput.scanReturn()
    with pytest.raises(SystemExit):
        badScan.scanReturn()
    assert goodScan.scanReturn()==0
