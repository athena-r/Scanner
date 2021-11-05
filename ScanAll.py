import yaml
import sys

class Scanner:

    def __init__(self,filename,dictionary='forbidden.yaml',badwords=[]):
        self.filename=filename
        self.dict=dictionary
        self.badwords=badwords

    def getData(self):
        try:
            with open(self.filename,'rb') as f:
                data=f.read()
        except FileNotFoundError as e:
            print("File was not found.")
            print(e)
            raise FileNotFoundError
        except Exception as e:
           print(e)
        else: 
            return data
        
    def getDict(self):
        try:
            self.badwords=[]
            with open(self.dict,'r') as d:
                data=yaml.load(d, Loader=yaml.Loader)
            for i in range(len(data)):
                self.badwords+= list(data.values())[i]
        except FileNotFoundError or OSError:
            print("You did not supply a dictionary. Please fix this.")
            raise FileNotFoundError
        except Exception as e:
            print("There was a problem loading the dictionary:")
            print(e)
            exit()
        else: 
            return self.badwords   

    def checkAll(self):
        try:
            badwords=self.getDict()
            self.matchedWords=0
            wordsFound=[]
            matchedEncodings=[]
            allEncodes=['ascii','utf-8','big5','big5hkscs','cp037','cp273','cp424','cp437','cp500','cp720','cp737','cp775','cp850','cp852','cp855','cp856','cp857','cp858',
                            'cp860','cp861','cp862','cp863','cp864','cp865','cp866','cp869','cp874','cp875','cp932','cp949','cp950','cp1006','cp1026','cp1125','cp1140',
                            'cp1250','cp1251','cp1252','cp1253','cp1254','cp1255','cp1256','cp1257','cp65001','euc_jp','euc_jis_2004','euc_jisx0213','euc_kr',
                            'gb2312','gbk','gb18030','hz','iso2022_jp','iso2022_jp_1','iso2022_jp_2','iso2022_jp_2004','iso2022_jp_3','iso2022_jp_ext','iso2022_kr',
                            'latin_1','iso8859_2','iso8859_3','iso8859_4','iso8859_5','iso8859_6','iso8859_7','iso8859_8','iso8859_9','iso8859_10','iso8859_11','iso8859_13',
                            'iso8859_14','iso8859_15','iso8859_16','johab','koi8_r','koi8_t','koi8_u','kz1048','mac_cyrillic','mac_greek','mac_iceland','mac_latin2',
                            'mac_roman','mac_turkish','ptcp154','shift_jis','shift_jis_2004','shift_jisx0213','utf_32','utf_32_be','utf_32_le','utf_16','utf_16_be',
                            'utf_16_le','utf_7','utf_8','utf_8_sig','cp1258']
            for e in allEncodes:
                newBytes=[b.encode(encoding=e,errors='replace') for b in badwords]
                for b in newBytes:
                    if (b in self.getData()) and (b):
                        if ((b.decode(encoding=e)) not in wordsFound) and ((b.decode(encoding=e))!='??'):
                            wordsFound.append(b.decode(encoding=e))
                            if e not in matchedEncodings: 
                                matchedEncodings.append(e)
                            print("Word matched with encoding "+e+": "+b.decode(encoding=e,errors='ignore'))
                            self.matchedWords+=1
        except UnicodeEncodeError or UnicodeDecodeError or UnicodeError:
            print("Issues with Unicode")
        except Exception as e:
            print("Other error: "+str(e))
            raise LookupError
        else:
            print("Number of matched words: "+str(self.matchedWords))
            print("Words found: "+str(wordsFound))
            print("Encodings matched" +str(matchedEncodings))
            if (self.matchedWords==0):
                print("No matching words found, program is clean.")
            return self.matchedWords
            
    def scanReturn(self):
        try:
            print(self.__dict__)
            self.checkAll()
        except Exception as e:
            print("Program failed.")
            if e!='':
                print('Exception information: '+str(type(e)))
            exit()
        else:
            return 0

if len(sys.argv)==2:
    file=sys.argv[1]
else: file='test5'

newScan=Scanner(str(file))
newScan.scanReturn()
