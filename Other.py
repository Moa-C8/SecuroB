import string
import random


def random_password(lenght):
        i = 0
        j = 0
        password = ""
        while i < lenght:
            j = random.randint(0, len(alphabet_plus)-1)
            password += alphabet_plus[j]
            i += 1
            
        return password

def random_password1(lenght):
        i = 0
        j = 0
        password = ""
        while i < lenght:
            j = random.randint(0, len(alphabet_plusMoinSpace)-1)
            password += alphabet_plusMoinSpace[j]
            i += 1
            
        return password

def readBgColor():
        fic = open(SettingFile, 'r')
        lines = fic.readlines()
        fic.close()
        lineBGSett = lines[0]
        valueBg = lineBGSett.replace('color,', '')
        valueBg = str(valueBg.replace('\n', ''))
        
        return valueBg
        
def readTreeviewColor():
        fic = open(SettingFile, 'r')
        lines = fic.readlines()
        fic.close()
        oddrowC = str(lines[3])
        oddrowC = oddrowC.replace('\n', "")
        evenrowC = str(lines[4])
        evenrowC = evenrowC.replace('\n', "")
        highlightC = str(lines[5])
        highlightC = highlightC.replace('\n', "")


        return oddrowC,evenrowC,highlightC

def readFgColor():
        fic = open(SettingFile, 'r')
        lines = fic.readlines()
        fic.close()
        ForegroundC = str(lines[6])
        ForegroundC = ForegroundC.replace('\n','')

        return ForegroundC

def appMainReader():
        fic = open(SettingFile, 'r')
        lines = fic.readlines()
        fic.close()
        application = str(lines[7])
        application = application.replace('\n', '')
        if application == "SecuroB":
                application = '1'
                return application
        elif application == "D&Crypt":
                application = '2'
                return application
        else:
                application = '3'
                return application


# couleur
dict_color = {0: "#35393C", 1: "#181818", 2: "#2E4053", 3: "#7D3C98", 4: "#1E8449", 5: "#C10202", 6: "#A93226", 7: "#5B5B5B", }

icone = 'media/SecurBoG.ico'

resolution = "1280x720"

basicInfos = 'media/BasicInfos.txt'
DCryptInfos = 'media/DCrypt infos.txt'
ManAssInfos = 'media/ManAssWord.txt'
TempFileDc = 'media/tempDatabase.db'
SettingFile = 'media/Settings.txt'

couleur_bg = readBgColor()
couleur_fg = readFgColor()

primary_color = readTreeviewColor()[0]
secondary_color = readTreeviewColor()[1]
highlight_color = readTreeviewColor()[2]

application = appMainReader()

rouge = "CC0000"
bleu = "0000CC"
vert = "33FF00"
jaune = "FFFF33"
orange = "FF6600"

# lettres
alphabet = string.ascii_letters
nombre = string.digits
alphabet_plusMoinSpace =list(string.ascii_letters + string.punctuation + string.digits)
alphabet_plus = list(string.ascii_letters + string.punctuation + string.digits + " ")
dictAlphabet = {}

maxCarMdp = 2

listExt = ['txt','csv','zip','aac','avi','doc','docx','gif','gz','h','htm','ico','iso','jpeg','mkv','mp3','mp4','odt','odp','ods',
'odg','pdf','png','pps','py','rar','tar','torrent','xls','xlsx','wav','xml','bat','bmp','exe','.sh']
