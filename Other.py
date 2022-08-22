import string
import random
import hashlib


def random_password(lenght, alpha):
        i = 0
        j = 0
        password = ""
        while i < lenght:
            j = random.randint(0, len(alphabet_plusMoinSpace)-1)
            password += alpha[j]
            i += 1
            
        return password

def readSettFile():
        fic = open(SettingFile, 'r')
        lines = fic.readlines()
        fic.close()

        return lines

def readBgColor():
        lines = readSettFile()

        lineBGSett = lines[0]
        valueBg = lineBGSett.replace('color,', '')
        valueBg = str(valueBg.replace('\n', ''))
        
        return valueBg
        
def readTreeviewColor():
        lines = readSettFile()

        oddrowC = str(lines[3])
        oddrowC = oddrowC.replace('\n', "")
        evenrowC = str(lines[4])
        evenrowC = evenrowC.replace('\n', "")
        highlightC = str(lines[5])
        highlightC = highlightC.replace('\n', "")


        return oddrowC,evenrowC,highlightC

def readFgColor():
        lines = readSettFile()
        
        ForegroundC = str(lines[6])
        ForegroundC = ForegroundC.replace('\n','')

        return ForegroundC

def genKey(password = "0"):
        if password == "0":
                password = random_password(15,alphabet_plus)
        liste_letter = []
        hash_ = hashlib.sha512(password.encode()).hexdigest()
        i = 0
        mot1 = ""
        mot2 = ""
        for each in hash_:
            liste_letter.append(each)
        while i < 64:
            mot1 += liste_letter[i]
            i += 1
        while i < 128:
            mot2 += liste_letter[i]
            i += 1
        mot1 = hashlib.sha256(mot1.encode()).hexdigest()
        mot2 = hashlib.sha256(mot2.encode()).hexdigest()
        key = mot2 + mot1
        key = hashlib.sha256(key.encode()).hexdigest()
        i = 0
        Lmot = list(key)
        while i < 21:  
            del Lmot[i]
            i += 1
        key = ""
        for each in Lmot:
            key += each
        key += "=" 
        key = key.encode('utf-8')

        return key


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

minCarMdp = 3

listExt = ['txt','csv','zip','aac','avi','doc','docx','gif','gz','h','htm','ico','iso','jpeg','mkv','mp3','mp4','odt','odp','ods',
'odg','pdf','png','pps','py','rar','tar','torrent','xls','xlsx','wav','xml','bat','bmp','exe','.sh']
