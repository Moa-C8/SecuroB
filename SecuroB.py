import tkinter as tk
from tkinter import filedialog, messagebox,colorchooser

from pathlib import Path
import hashlib
import cryptography
from cryptography.fernet import Fernet
import random
import sqlite3
from os import remove,execv
import sys

from Other import *
from DeCrypt import AppDeCrypt
from PassMan import AppSecuroB


def setting_window(self):       
        self.setWindow = tk.Toplevel()
        self.setWindow.geometry("500x400")

        self.setWindow.protocol("WM_DELETE_WINDOW", lambda:setClose(self))
        
        self.setWindow.config(bg=couleur_bg)
        self.setWindow.title('SecurBoG settings')
        self.setWindow.iconbitmap(icone)
        self.setWindow.resizable(width=False, height=False)

        readSettingsFile(self)

        StartMessageframe = tk.Frame(self.setWindow, bg=couleur_bg, width=500, height=50)
        SMCan = tk.Canvas(StartMessageframe, bg=couleur_bg, highlightthickness=0, width=500, height=50).grid(columnspan=4, rowspan=1)

        lblmessageStart = tk.Label(StartMessageframe, text="Starting message", bg=couleur_bg, fg=couleur_fg, font=("impact", 16)).grid(column=0, row=0)
        self.lblVSM = tk.StringVar()

        if self.listLineSett[1] == "starting_message,0\n":
            self.lblVSM.set('Enable it')
        elif self.listLineSett[1] == "starting_message,1\n":
            self.lblVSM.set('Disable it')

        SMbutton = tk.Button(StartMessageframe,textvariable=self.lblVSM, pady=2, relief='groove', padx=2, bg=couleur_bg, bd=3, fg=couleur_fg, command=lambda:change_settingsFile(self,"StartMessage")).grid(column=2, row=0)

        BtnColorFrame = tk.Frame(self.setWindow, bg=couleur_bg, width=500, height=280)
        btnCan = tk.Canvas(BtnColorFrame, bg=couleur_bg, highlightthickness=0, width=500, height=280).grid(columnspan=7, rowspan=4)

        lblBtnCcolor = tk.Label(BtnColorFrame, text="Change bg color", bg=couleur_bg, fg=couleur_fg, font=("impact", 16)).place(x=34, y=40)
        
        btnColor0 = tk.Button(BtnColorFrame, text='Black',width=6 , relief='groove', bg='#181818', fg=couleur_fg, command=lambda:change_settingsFile(self,'bgColor','#181818')).grid(column=0,row=1)
        btnColor1 = tk.Button(BtnColorFrame, text='Blue',width=6 , relief='groove', bg='#2E4053', fg=couleur_fg, command=lambda:change_settingsFile(self,'bgColor','#2E4053')).grid(column=2,row=1)
        btnColor2 = tk.Button(BtnColorFrame, text='Purple',width=6 , relief='groove', bg='#7D3C98', fg=couleur_fg, command=lambda:change_settingsFile(self,'bgColor','#7D3C98')).grid(column=4,row=1)
        btnColor3 = tk.Button(BtnColorFrame, text='Green',width=6 , relief='groove', bg='#1E8449', fg=couleur_fg, command=lambda:change_settingsFile(self,'bgColor','#1E8449')).grid(column=6,row=1)
        btnColor4 = tk.Button(BtnColorFrame, text='Red',width=6 , relief='groove', bg='#C10202', fg=couleur_fg, command=lambda:change_settingsFile(self,'bgColor','#C10202')).grid(column=0,row=2)
        btnColor5 = tk.Button(BtnColorFrame, text='Orange',width=6 , relief='groove', bg='#A93226', fg=couleur_fg, command=lambda:change_settingsFile(self,'bgColor','#A93226')).grid(column=2,row=2)
        btnColor6 = tk.Button(BtnColorFrame, text='Grey',width=6 , relief='groove', bg='#5B5B5B', fg=couleur_fg, command=lambda:change_settingsFile(self,'bgColor','#5B5B5B')).grid(column=4,row=2)
        btnColor7 = tk.Button(BtnColorFrame, text='Basic',width=6 , relief='groove', bg='#35393C', fg=couleur_fg, command=lambda:change_settingsFile(self,'bgColor','#35393C')).grid(column=6,row=2)
        btnColor8 = tk.Button(BtnColorFrame, text='Perso color' , relief='groove', bg=couleur_bg, fg=couleur_fg, command=lambda:persoBgColor(self)).grid(column=2,row=3)
        btnColor9 = tk.Button(BtnColorFrame, text='Perso Fg' , relief='groove', bg=couleur_bg, fg=couleur_fg, command=lambda:persoFgColor(self)).grid(column=4,row=3)

        StartMessageframe.grid(column=1, row=1)
        BtnColorFrame.grid(column=1, row=2)
        
        self.setWindow.mainloop()

def readSettingsFile(self):
        fic = open(SettingFile, 'r')
        self.listLineSett = fic.readlines()
        fic.close()

def setClose(self):
        self.setWindow.destroy()
        if messagebox.askyesno('Restart app', 'do you want to restart the app \nto apply the changes') == True:
            # Fonctionne que avec le exe
            sys.stdout.flush() 
            execv(sys.argv[0], sys.argv )
# colors Fonction
def persoBgColor(self):
        persoColor = colorchooser.askcolor()[1]
        if persoColor:
            self.change_settingsFile('bgColor', str(persoColor))

def persoFgColor(self):
        persofg = colorchooser.askcolor()[1]
        if persofg:
            self.change_settingsFile('fg', str(persofg))

def change_settingsFile(self, setting, value="0"):

        if setting == "bgColor":
            self.listLineSett[0] = (f'{value}\n')      
        elif setting == "StartMessage":
            if self.listLineSett[1] == "starting_message,0\n":
                value = 1
                self.lblVSM.set('Disable it')
            elif self.listLineSett[1] == "starting_message,1\n":
                value = 0 
                self.lblVSM.set('Enable it')
            self.listLineSett[1] = (f'starting_message,{value}\n')
        elif setting == "language":
            self.listLineSett[2] = (f'language,{value}\n')
        elif setting == 'fg':
            self.listLineSett[6] = (f'{value}\n')
        elif setting == 'DefaultApp':
            self.listLineSett[7] =(f'{value}\n')
        
        fic = open(SettingFile, 'w')
        for each in self.listLineSett:
            fic.write(each) 
        fic.close()
    # Fenetre Info
def infoAWindow(self, what):
        self.InfoWindow = tk.Toplevel()
        self.InfoWindow.geometry("500x600")
        self.InfoWindow.config(bg=couleur_bg)
        
        self.InfoWindow.iconbitmap(icone)
        self.InfoWindow.resizable(width=False, height=False)

        if what == '0':
            textFile = open(basicInfos)
            self.InfoWindow.title('SecuroB Main Infos')
        elif what == '1':
            textFile = open(DCryptInfos)
            self.InfoWindow.title('SecuroB D&Crypt Infos')
        elif what == '2':
            textFile = open(ManAssInfos)
            self.InfoWindow.title('SecuroB Infos')
        TxtContent = textFile.read()
        textFile.close()

        textIBox = tk.Text(self.InfoWindow, height=35, width=70,bg=couleur_bg, font=("Raleway", 15), fg=couleur_fg, padx=2, pady=2)
        textIBox.insert(1.0, TxtContent)
        textIBox.tag_configure('center', justify='center')
        textIBox.tag_add('center', 1.0, 'end')
        textIBox.pack()

        self.InfoWindow.mainloop()
    # Fenetre Top level Create key by Password
def keyFileByPswd(self):
        self.window2 = tk.Toplevel(self)
        self.window2.title("File Key by password")
        self.window2.iconbitmap(icone)
        self.window2.config(bg=couleur_bg)
        self.window2.geometry('400x200')


        framepswd = tk.LabelFrame(self.window2, text='Password', fg=couleur_fg, bg=couleur_bg)
        framepswd.pack(padx=10, pady=10)

        self.labelEntry2 = tk.Label(framepswd, bg=couleur_bg, fg=couleur_fg ,font=('Raleway', 18))
        self.labelEntry2.grid(column=0, row=0)

        self.seeTxt = tk.StringVar()

        self.entrypswd = tk.Entry(framepswd, font=('Raleway', 18), show='*')
        self.entrypswd.grid(column=0, row=1)

        self.btnHideSee = tk.Button(framepswd, textvariable=self.seeTxt, bg=couleur_bg, relief='groove', fg=couleur_fg, borderwidth=5 ,padx=1, pady=1, command=lambda:self.ShowEntryPswd())
        self.btnHideSee.grid(column=2, row=1)
        self.seeTxt.set("see")

        self.entrypswd.bind('<Return>', self.afterKfile)

        self.btnCreate = tk.Button(self.window2, text="Create", bg=couleur_bg, fg=couleur_fg, relief='groove', command=lambda:self.afterKfile(1))
        self.btnCreate.pack()
   
   
def keyFileByKey(self):
        self.window4 = tk.Toplevel(self)
        self.window4.title("File Key by key")
        self.window4.iconbitmap(icone)
        self.window4.config(bg=couleur_bg)
        self.window4.geometry('380x150')

        self.txt = tk.Label(self.window4, text='make your key file with a key', fg=couleur_fg, bg=couleur_bg, font=('Raleway', 14))
        self.txt.pack(pady=5)

        LabelFKey = tk.LabelFrame(self.window4, bg=couleur_bg, highlightthickness=0, height=100)
        LabelFKey.pack(padx=5)

        self.errorTxt = tk.StringVar()

        #self.labelTbox = tk.Label(self.window2, text='Entry key \n44 char with = at the end', bg=couleur_bg, fg=couleur_fg ,font=('Raleway', 14))
        #self.labelTbox.pack()
        self.EntryKey = tk.Entry(LabelFKey, width=245, font=('Raleway', 12))
        self.EntryKey.pack()
        self.TxtError = tk.Label(LabelFKey, bg=couleur_bg, fg=couleur_fg ,font=('Raleway', 16))
        self.TxtError.pack(pady=5)

        #self.EntryKey.bind('<Return>', lambda:afterKbyK(self))

        self.btnCreateK = tk.Button(self.window4, text="Create", bg=couleur_bg, fg=couleur_fg, relief='groove', command=lambda:afterKbyK(self,8))
        self.btnCreateK.pack(pady=10)

def ShowEntryPswd(self):
        global l
        if l == 0:
            self.entrypswd.config(show="")
            l += 1
            self.seeTxt.set('hide')
        else:
            self.entrypswd.config(show="*")
            l = 0
            self.seeTxt.set('see')

def afterKbyK(self,e):
        key = self.EntryKey.get()
        lenTxt = len(key)
        if lenTxt < 44:
            self.TxtError.configure(text="wrong key")
        else:
            liste = []
            for i in key:
                liste.append(i)
            if liste[43] != "=":
                self.TxtError.configure(text="wrong key")
            else:
                try:
                    filekey = filedialog.asksaveasfile(title="Create key",filetypes=[("key files","*.key")], defaultextension=".key", initialfile="Mykey")
                except:
                    pass
                else:
                    try:
                        filela = open(filekey.name, "wb")
                    except:
                        pass
                    else:
                        key = bytes(key, 'utf-8')
                        filela.write(key)
                        filela.close()

def afterKfile(self,e):
        password = self.entrypswd.get()
        lenPswd = len(password)
        if lenPswd <= 7:
            self.labelEntry2.configure(text='min 8 lenght')
        elif lenPswd > 7:
            self.labelEntry2.configure(text='Ok')

            key = AppDeCrypt.gen_key_by_password(application, password)
            
            try:
                fileKey = filedialog.asksaveasfile(title="Create key",filetypes=[("key files","*.key")], defaultextension=".key", initialfile="Mykey")
            except:
                pass
            else:
                try:
                    filele = open(fileKey.name, "wb")
                except:
                    pass
                else:
                    filele.write(key)
                    filele.close()
                    self.window2.deiconify()
                    self.labelEntry2.configure(text='you can close me')
    # Fenetre Top level generate password
def passwordGenerator(self):
        window3 = tk.Toplevel(self)
        window3.title("Password Generator")
        window3.iconbitmap(icone)
        window3.config(bg=couleur_bg)
        window3.geometry('400x200') 


        frameGenerator = tk.Frame(window3, bg=couleur_bg, height=100)
        frameGenerator.pack(padx=10,pady=10)

        canGen = tk.Canvas(frameGenerator, bg=couleur_bg, highlightthickness=0, height=100).grid(columnspan=4, rowspan=3)

        self.lblSizeLeft = tk.Label(frameGenerator,text='Size', bg=couleur_bg, fg=couleur_fg ,font=('Raleway', 18))
        self.lblSizeLeft.grid(column=0, row=0)

        self.entrySize = tk.Entry(frameGenerator,width=5,text="Size", font=('Raleway', 15))
        self.entrySize.grid(column=1, row=0)
        BtnGenerate = tk.Button(frameGenerator, text="Generate", bg=couleur_bg, fg=couleur_fg, relief='groove', command=lambda:self.CheckGenerate('1')).grid(column=3, row=0) 

        self.TxtBoxPswd = tk.Text(window3, height=3, width=250, padx=2, pady=2, state='normal')
        self.TxtBoxPswd.pack(padx=10, pady=10)

        self.entrySize.bind('<Return>',self.CheckGenerate)

def CheckGenerate(self, e):
        size = self.entrySize.get()
        
        if size.isdigit() == True:
            size = int(size)

            if size <= 10000:
                self.lblSizeLeft.configure(text='Ok')              
                password = random_password1(size)

                self.TxtBoxPswd.delete(1.0, "end")
                self.TxtBoxPswd.insert(1.0, password)
            elif size > 10000:
                self.lblSizeLeft.configure(text="Max 10000")
        else:
            self.lblSizeLeft.configure(text='number only')

#Menu

def menuDeCrypt(app):
    menuDecrypt = tk.Menu(app, bd=2, font=("Raleway", 16), relief='sunken')

    menuA = tk.Menu(menuDecrypt, tearoff=0)
    menuDecrypt.add_cascade(label="App", font=("Raleway", 16), menu=menuA)

    menuF = tk.Menu(menuDecrypt, tearoff=0)
    menuDecrypt.add_cascade(label="Folder", font=("Raleway", 16), menu=menuF)

    menuI = tk.Menu(menuDecrypt, tearoff=0)
    menuDecrypt.add_cascade(label="Infos", font=("Raleway", 16), menu=menuI)

    
    menuDecrypt.add_cascade(label="Settings", font=("Raleway", 10), command=lambda:setting_window(app))

    menuA.add_command(label="Password manager", font=("Raleway", 10), command=lambda:mainToSecurob(app))
    #menuA.add_command(label="Main menu", font=("Raleway", 10), command=lambda:mainMenu(app))
    
    menuF.add_command(label="Password Generator", font=("Raleway", 10), command=lambda:passwordGenerator(app))
    menuF.add_separator()
    menuF.add_command(label="Create key file Random", font=("Raleway", 10), command=lambda:AppDeCrypt.key_generator_random(app))
    menuF.add_command(label="Create key file by Password", font=("Raleway", 10), command=lambda:keyFileByPswd(app))
    menuF.add_command(label="Create key file with key", font=("Raleway", 10), command=lambda:keyFileByKey(app))

    menuI.add_command(label="Basic Infos", font=("Raleway", 10), command=lambda:infoAWindow(app,'0'))
    menuI.add_separator()
    menuI.add_command(label="Infos D&Crypt", font=("Raleway", 10), command=lambda:infoAWindow(app,'1')) 
    menuI.add_command(label="Infos Password manager", font=("Raleway", 10), command=lambda:infoAWindow(app,'2'))
            
    app.config(menu=menuDecrypt)

def menuSecuroB(app):
        menuPswdmanager = tk.Menu(app, bd=2, font=("Raleway", 16), relief='sunken')

        menuA = tk.Menu(menuPswdmanager, tearoff=0)
        menuPswdmanager.add_cascade(label="App", font=("Raleway", 16), menu=menuA)

        menuF = tk.Menu(menuPswdmanager, tearoff=0)
        menuPswdmanager.add_cascade(label="Folder", font=("Raleway", 16), menu=menuF)

        menuI = tk.Menu(menuPswdmanager, tearoff=0)
        menuPswdmanager.add_cascade(label="Infos", font=("Raleway", 16), menu=menuI)

        menuS = tk.Menu(menuPswdmanager, tearoff=0)
        menuPswdmanager.add_cascade(label="Settings", font=("Raleway", 16), menu=menuS)

        menuSearch = tk.Menu(menuPswdmanager, tearoff=0)
        menuPswdmanager.add_cascade(label="Search", font=("Raleway", 16), menu=menuSearch)

        menuA.add_command(label="(De)Crypt Folder", font=("Raleway", 10), command=lambda:mainToDeCrypt(app))
        #menuA.add_command(label="Main menu", font=("Raleway", 10), command=lambda:mainMenu(app))
        
        menuF.add_command(label="Password Generator", font=("Raleway", 10), command=lambda:passwordGenerator(app))
        menuF.add_separator()
        menuF.add_command(label="Create key file Random", font=("Raleway", 10), command=lambda:AppDeCrypt.key_generator_random(app))  #, command=DeCrypt.key_generator_random
        menuF.add_command(label="Create key file by Password", font=("Raleway", 10), command=lambda:keyFileByPswd(app))
        menuF.add_command(label="Create key file with key", font=("Raleway", 10), command=lambda:keyFileByKey(app))
        menuF.add_separator()
        menuF.add_command(label="Create Password manager file", font=("Raleway", 10), command=createDbc)

        menuI.add_command(label="Basic Infos", font=("Raleway", 10), command=lambda:infoAWindow(app,'0'))
        menuI.add_separator()
        #menuI.add_command(label="Infos D&Crypt", font=("Raleway", 10), command=lambda:infoAWindow(app,'1')) 
        menuI.add_command(label="Infos Password manager", font=("Raleway", 10), command=lambda:infoAWindow(app,'2'))

        menuS.add_command(label="Basic settings", font=("Raleway", 10), command=lambda:setting_window(app))
        menuS.add_separator()
        menuS.add_command(label="Primary Color", font=("Raleway", 10), command=lambda:AppSecuroB.primaryColor(app))           
        menuS.add_command(label="Secondary Color", font=("Raleway", 10), command=lambda:AppSecuroB.secondaryColor(app))       
        menuS.add_command(label="Highlight Color", font=("Raleway", 10), command=lambda:AppSecuroB.highlightColor(app))     

        menuSearch.add_command(label="Search in Treeview", font=("Raleway", 10), command=lambda:AppSecuroB.lookupRecords(app))                                  
        menuSearch.add_separator()
        menuSearch.add_command(label="Reset Treeview", font=("Raleway", 10), command=lambda:AppSecuroB.querryDataBase(app))                          

        app.config(menu=menuPswdmanager)

#database

def createDbc():
    try: 
        fileKey = filedialog.askopenfile(title='Select a key file', filetypes=[("Key File", "*.key")])
        pathKey = fileKey.name
    except:
        pass
    else:
        try:
            dbNCrypt = filedialog.asksaveasfile(title='Create Folder', filetypes=[("Password Manager")], initialfile=('My Manager'), defaultextension=".db")
        except:
            pass
        else:
            try:
                pathFile = dbNCrypt.name
            except:
                messagebox.showerror('error', 'you have not finalized the creation of \nyour crypted database')
            else:
                fileKey = open(pathKey, 'rb')
                key = fileKey.read()
                fileKey.close()
                try:
                    fer = Fernet(key)
                except:
                    messagebox.showerror('error', 'problem with key file')
                else:
                    AppSecuroB.createTable(path=pathFile, self=application)
                    
                    dbNCrypt = open(pathFile, 'rb')
                    TxtDb = dbNCrypt.read()
                    dbNCrypt.close()

                    remove(pathFile)

                    pathFile += 'c'
                    txtDCryptDb = fer.encrypt(TxtDb)
                    
                    fFile = open(pathFile, 'wb')
                    fFile.write(txtDCryptDb)
                    fFile.close()

                    messagebox.showinfo('great',"you create a manager password file .dbc \nit's linked to the key used don't loose it")

def removeDb():
    try:
        remove('media/tempDatabase.db')
    except:
        pass

if __name__ == '__main__':
    def mainToDeCrypt(app):
        removeDb()
        app.destroy()
        
        app = AppDeCrypt()
        menuDeCrypt(app)
        app.protocol("WM_DELETE_WINDOW", lambda:closeAppWindow2(app))
            
    def mainToSecurob(app):
        removeDb()
        app.destroy()

        app = AppSecuroB()
        menuSecuroB(app)
        app.protocol("WM_DELETE_WINDOW", lambda:closeAppWindow2(app))

    def closeAppWindow2(app):
        if messagebox.askyesno("Close App","do you correctly save all ?") == True:
            removeDb()
            app.destroy()

    if application == '2':
        application = AppDeCrypt()
        menuDeCrypt(application)
        application.protocol("WM_DELETE_WINDOW",lambda:closeAppWindow2(application))
    else:
        application = AppSecuroB()
        menuSecuroB(application)
        application.protocol("WM_DELETE_WINDOW",lambda:closeAppWindow2(application))
    
    application.mainloop()