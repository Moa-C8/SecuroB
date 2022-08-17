import tkinter as tk 
from tkinter import ttk,messagebox,colorchooser, filedialog

import sqlite3 
from pathlib import Path
from cryptography.fernet import Fernet
from os import remove
import hashlib

from Other import *

class AppSecuroB(tk.Tk):
    
    def __init__(self):
        super().__init__()
        
        self.geometry(resolution)
        self.config(bg=couleur_bg)
        self.title('SecuroB  -Password Manager')
        self.iconbitmap(icone)
        self.resizable(width=False, height=False)

        self.MainFrame()
        self.protocol("WM_DELETE_WINDOW", self.SavageClose)
        
        self.readSettingsFile()

        if self.listLineSett[1] == "starting_message,1\n":
            messagebox.showinfo('Infos', 'if you never use this app or if you \n had some problems. \nGo on infos in the menu bar \nyou can desactivate this message in settings')
        

    def MainFrame(self):
        self.config(bg=couleur_bg)
        self.style = ttk.Style()
        #pick a theme
        self.style.theme_use('default')

        self.style.configure('Treeview', 
        background='#D3D3D3', foreground="black", 
        fieldbackground='#D3D3D3')

        #change selecetd color
        self.style.map('Treeview', background=[('selected', highlight_color)])

        self.name_app = tk.Label(self, text="SecuroB", font=("Impact", 40), bg=couleur_bg, fg=couleur_fg).place(x=10, y=10)

        # create treeview frame (easier for scrollbar)
        self.treeFrame = tk.Frame(self)
        
        #create a treeview scrollbar
        self.treeScroll = tk.Scrollbar(self.treeFrame)
        self.treeScroll.pack(side='right', fill='y')

        #create treeview
        self.myTree = ttk.Treeview(self.treeFrame, height=24,yscrollcommand=self.treeScroll.set, selectmode="extended")
        self.myTree.pack()

        #configure scrollbar
        self.treeScroll.config(command=self.myTree.yview)

        #define our columns
        self.myTree['columns'] = ('siteOrApp','email', 'password', 'id')

        #format our columns
        self.myTree.column('#0', width=0, stretch='no')
        self.myTree.column("siteOrApp", width=140, anchor='w')
        self.myTree.column("email", width=240, anchor='w')
        self.myTree.column("password", width=420, anchor='w')
        self.myTree.column("id", width=30, anchor='center')

        self.myTree.heading("#0", text="", anchor='center')
        self.myTree.heading("siteOrApp", text="Site or App name", anchor='center')
        self.myTree.heading("email", text="Email or Username", anchor='center')
        self.myTree.heading("password", text="Password or Key", anchor='center')
        self.myTree.heading("id", text="Id", anchor='center')

        #create a striped row tags
        self.myTree.tag_configure('oddrow', background=primary_color)
        self.myTree.tag_configure('evenrow', background=secondary_color)

        self.frameFile = tk.LabelFrame(self, text="File", background=couleur_bg, fg=couleur_fg)
        self.frameFile.pack(expand='yes',padx=20, pady=(50,0))

        self.keyBtnText = tk.StringVar()
        self.fileBrowseText = tk.StringVar()
        self.openTextBtn = tk.StringVar()

        self.SaveExitTxtBtn = tk.StringVar()

        self.btnSaveExit = tk.Button(self,textvariable=self.SaveExitTxtBtn, bg=couleur_bg, relief='groove', bd=3, fg=couleur_fg, padx=2, pady=2, command=self.cryptDbFile)
        self.SaveExitTxtBtn.set("Save and \nclose treeview")
        self.btnSaveExit.place(x=1130, y=645)       

        self.lblKey = tk.Label(self.frameFile, text="", font=("Raleway", 16), bg=couleur_bg, fg=couleur_fg)
        self.lblKey.grid(row=0, column=0, padx=10, pady=(3,5))
        self.btnKey = tk.Button(self.frameFile,textvariable=self.keyBtnText, bg=couleur_bg, relief='groove', bd=3, fg=couleur_fg, padx=2, pady=2, command=self.find_key)
        self.keyBtnText.set("Browse Key")
        self.btnKey.grid(row=0, column=1, pady=(3,3))

        self.lblBrowse = tk.Label(self.frameFile, text="", font=("Raleway", 16), bg=couleur_bg, fg=couleur_fg)
        self.lblBrowse.grid(row=0, column=2, padx=10, pady=(3,5))
        self.btnBrowse = tk.Button(self.frameFile,textvariable=self.fileBrowseText, bg=couleur_bg, relief='groove', bd=3, fg=couleur_fg, padx=2, pady=2, command=self.find_database)
        self.fileBrowseText.set("Browse Database")
        self.btnBrowse.grid(row=0, column=3, pady=(3,5), padx=(0,5))

        self.btnOpen = tk.Button(self.frameFile, textvariable=self.openTextBtn, bg=couleur_bg, relief='groove', bd=3, fg=couleur_fg, padx=2, pady=2, command=self.afterBtnOpen)
        self.openTextBtn.set("Open")

        self.buttonFrame = tk.LabelFrame(self, text='Commands', bg=couleur_bg, fg=couleur_fg)
        self.buttonFrame.pack(expand='yes', padx=20, pady=(0,0))

        # ADD Record Entry Boxes
        self.dataFrame = tk.LabelFrame(self, text="record", bg=couleur_bg, fg=couleur_fg)
        self.dataFrame.pack(expand='yes', padx=20, pady=(0,0))
        #affichage Treeview Frame
        self.treeFrame.pack(pady=(10,10))

        self.labelSiteName = tk.Label(self.dataFrame, text="Site or App name", bg=couleur_bg, fg=couleur_fg)
        self.labelSiteName.grid(row=0, column=0, padx=10, pady=(2,4))
        self.entrySiteName = tk.Entry(self.dataFrame)
        self.entrySiteName.grid(row=0, column=1, padx=10, pady=(2,4))

        self.labelEmail = tk.Label(self.dataFrame, text="Email or Username", bg=couleur_bg, fg=couleur_fg)
        self.labelEmail.grid(row=0, column=2, padx=10, pady=(2,4))
        self.entryEmail = tk.Entry(self.dataFrame)
        self.entryEmail.grid(row=0, column=3, padx=10, pady=(2,4))

        self.labelPswd = tk.Label(self.dataFrame, text="Password or Key", bg=couleur_bg, fg=couleur_fg)
        self.labelPswd.grid(row=0, column=4, padx=10, pady=(2,4))
        self.entryPswd = tk.Entry(self.dataFrame)
        self.entryPswd.grid(row=0, column=5, padx=10, pady=(2,4))

        self.id_entry = tk.Entry(self, background=couleur_bg)
        self.id_entry.place(x=1200, y =740)

        # addbutton


        self.btnUpdate = tk.Button(self.buttonFrame,text="Update Records", bg=couleur_bg, fg=couleur_fg, relief='groove', bd=3, command=self.updateRecords)
        self.btnUpdate.grid(row=0, column=0, padx=10, pady=(5, 5))

        self.btnAdd = tk.Button(self.buttonFrame,text="Add Record", bg=couleur_bg, fg=couleur_fg, relief='groove', bd=3, command=self.addRecord)
        self.btnAdd.grid(row=0, column=1, padx=10, pady=(5, 5))

        self.btnRemoveSelected = tk.Button(self.buttonFrame,text="Remove selected", bg=couleur_bg, relief='groove', bd=3, fg=couleur_fg, command=self.removeSelected)
        self.btnRemoveSelected.grid(row=0, column=4, padx=10, pady=(5, 5))

        self.btnRemoveAll = tk.Button(self.buttonFrame,text="Remove all", bg=couleur_bg, fg=couleur_fg, relief='groove', bd=3, command=self.removeAll)
        self.btnRemoveAll.grid(row=0, column=5, padx=10, pady=(5, 5))

        self.btnClear = tk.Button(self.buttonFrame, text="Clear Entry Boxes", bg=couleur_bg, fg=couleur_fg, relief='groove', bd=3, command=self.clearEntries)
        self.btnClear.grid(row=0, column=2, padx=10, pady=(5, 5))

        self.btnRTreeview = tk.Button(self.buttonFrame, text="Update Treview", bg=couleur_bg, fg=couleur_fg, relief='groove', bd=3, command=self.querryDataBase)
        self.btnRTreeview.grid(row=0, column=3, padx=10, pady=(5, 5))

        self.myTree.bind("<ButtonRelease-1>", self.select_record)

    # Fonction for Treeview 
    def select_record(self, event): 
        self.clearEntries()
        #grab recors Number and values
        selected = self.myTree.focus()
        values = self.myTree.item(selected, 'values')
        #output to entry boxes
        try:
            self.entrySiteName.insert(0, values[0])
        except:
            pass
        else:
            self.entryEmail.insert(0, values[1])
            self.entryPswd.insert(0, values[2])
            self.id_entry.insert(0, values[3])

    def clearEntries(self):
        self.entrySiteName.delete(0, 'end')
        self.entryEmail.delete(0, 'end')
        self.entryPswd.delete(0, 'end')
        self.id_entry.delete(0, 'end')

    def up(self):
        rows = self.myTree.selection()
        for row in rows:
            self.myTree.move(row, self.myTree.parent(row), self.myTree.index(row)-1)

    def down(self):
        rows = self.myTree.selection()
        for row in reversed(rows):
            self.myTree.move(row, self.myTree.parent(row), self.myTree.index(row)+1)
  
    def removeSelected(self):
        if messagebox.askyesno("Are you sure", "you will delete all your selected data \nare you sure") == True:
            x = self.myTree.selection()
            
            listIDelete = []
            #loop
            for record in x:
                listIDelete.append(self.myTree.item(record, 'values')[3])

            for record in x:
                self.myTree.delete(record)
            try:
                conn = sqlite3.connect(self.absDCPathdatabase)
            except:
                pass
            else: 
                c = conn.cursor()

                c.executemany("DELETE FROM myData WHERE id = ?", [(a,) for a in listIDelete])

                #Delete From Database
                c.execute("")

                conn.commit()
                conn.close()

                self.clearEntries()
        
    def removeAll(self):
        try:
            conn = sqlite3.connect(self.absDCPathdatabase)
        except:
            pass
        else:
            c = conn.cursor()

            if messagebox.askyesno("Are you sure", "you will delete all your data \nare you sure") == True:
                for record in self.myTree.get_children():
                    self.myTree.delete(record)
                #Delete From Database
                c.execute("DROP TABLE myData")

            conn.commit()
            conn.close()

            self.clearEntries()
            self.createTable(self.absDCPathdatabase)
    # Fonction with databases

    def updateRecords(self):
        selected = self.myTree.focus()
        #update record
        self.myTree.item(selected, text="", values=(self.entrySiteName.get(), self.entryEmail.get(), self.entryPswd.get(), self.id_entry.get(),))
        #update database
        try:
            conn = sqlite3.connect(self.absDCPathdatabase)
        except:
            pass
        else:   
            c = conn.cursor()

            c.execute("""UPDATE myData SET
            siteOrApp = :siteOrApp,
            email = :email,
            password = :password

            WHERE oid = :oid""",
            {
                'siteOrApp': self.entrySiteName.get(),
                'email': self.entryEmail.get(),
                'password': self.entryPswd.get(),
                'oid':self.id_entry.get(),
            })

            conn.commit()
            conn.close()

            self.clearEntries()
        
    def querryDataBase(self):
        try:
            self.createTable(self.absDCPathdatabase)
        except:
            pass

        for record in self.myTree.get_children():
            self.myTree.delete(record)
        try:
            conn = sqlite3.connect(self.absDCPathdatabase)
        except:
            print("soucis")
        else:
            curs = conn.cursor()
            curs.execute('SELECT rowid, * FROM myData')
            records = curs.fetchall()

            global count
            count = 0

            for record in records:
                if count %2 == 0:
                    self.myTree.insert(parent='', index='end', iid=count, text='', values=(record[1],record[2],record[3],record[0]), tags=('evenrow',))
                else:
                    self.myTree.insert(parent='', index='end', iid=count, text='', values=(record[1],record[2],record[3],record[0]), tags=('oddrow',))
                count += 1

            conn.commit()
            conn.close()

    def addRecord(self):
        #update database
        try:
            conn = sqlite3.connect(self.absDCPathdatabase)
        except:
            pass
        else:
            c = conn.cursor()

            #add new record

            request1 = "INSERT INTO myData (siteOrApp, email, password) values (?, ?, ?) "

            c.execute(request1,(self.entrySiteName.get(), self.entryEmail.get(), self.entryPswd.get()))

            conn.commit()
            conn.close()

            self.clearEntries()

            #clear the treeview table
            self.myTree.delete(*self.myTree.get_children())

            self.querryDataBase()

    def createTable(self, path):
        try:
            conn = sqlite3.connect(path)           
        except:
            pass
        else:
            curs = conn.cursor()
            #create Table
            curs.execute("""CREATE TABLE if not exists myData (
                siteOrApp text,
                email text,
                password text,
                id INTEGER PRIMARY KEY AUTOINCREMENT)
            """)

            #commit changes
            conn.commit()

            conn.close()

    def readSettingsFile(self):
        fic = open(SettingFile, 'r')
        self.listLineSett = fic.readlines()
        fic.close()

    def lookupRecords(self):
        global entrySearch, search
        search = tk.Toplevel(self)
        search.title("Lookup Records")
        search.iconbitmap(icone)
        search.config(background=couleur_bg)
        search.geometry('400x250')

        # Create Label
        search_frame = tk.LabelFrame(search, text='Site or App name', fg=couleur_fg, bg=couleur_bg)
        search_frame.pack(padx=10, pady=10)

        

        entrySearch = tk.Entry(search_frame, font=('Raleway', 18))
        entrySearch.pack(padx=20, pady=20)
        entrySearch.bind("<Return>", self.searchRecords)

        btnSearch = tk.Button(search, text="search", bg=couleur_bg, fg=couleur_fg, command=lambda:self.searchRecords(1))
        btnSearch.pack(padx=10, pady=10)

    def searchRecords(self, e):
        lookupRecord = entrySearch.get()
        self.querryDataBase()
        # Close search windows
        search.destroy()
        for record in self.myTree.get_children():
            self.myTree.delete(record)
        try:
            conn = sqlite3.connect(self.absTempDb)
        except:
            pass
        else:
            curs = conn.cursor()
            #request2 = 
            curs.execute("SELECT rowid, * FROM myData WHERE siteOrApp like ? ", (lookupRecord,))
            records = curs.fetchall()

            global count
            count = 0

            for record in records:
                if count %2 == 0:
                    self.myTree.insert(parent='', index='end', iid=count, text='', values=(record[1],record[2],record[3],record[0]), tags=('evenrow',))
                else:
                    self.myTree.insert(parent='', index='end', iid=count, text='', values=(record[1],record[2],record[3],record[0]), tags=('oddrow',))
                count += 1

            conn.commit()
            conn.close()

    #Fonction for colors options
    def primaryColor(self):
        self.readSettingsFile()
        primary_color = colorchooser.askcolor()[1]
        
        if primary_color:
            self.listLineSett[3] = (f'{primary_color}\n')
            self.myTree.tag_configure('evenrow', background=primary_color)
            self.changeSettingColor()

    def secondaryColor(self):
        self.readSettingsFile()
        secondary_color = colorchooser.askcolor()[1]
        
        if secondary_color:
            self.listLineSett[4] = (f'{secondary_color}\n')
            self.myTree.tag_configure('oddrow', background=secondary_color)
            self.changeSettingColor()

    def highlightColor(self):
        self.readSettingsFile()
        highlight_color = colorchooser.askcolor()[1]
        
        if highlight_color:
            self.listLineSett[5] = (f'{highlight_color}\n')
            self.style.map('Treeview', background=[('selected', highlight_color)])
            self.changeSettingColor()

    def changeSettingColor(self):
        fic = open(SettingFile, 'w')
        for each in self.listLineSett:
            fic.write(each)
        fic.close()

    # Other Fonction
    def openTVBtn(self):
        if self.lblKey.cget("text") != "" and self.lblBrowse.cget("text") != "" :
            self.btnOpen.grid(row=0, column=4, pady=(3,5), padx=(5,5))
 
    def get_name(self, file_Abs_path):
        path = Path(file_Abs_path)
        name_file = path.name

        return name_file
    
    def find_key(self):
        self.keyBtnText.set("Browse ...")
        try :
            filekey = filedialog.askopenfile(title="Select key",filetypes=[("Key file", "*.key")])
            self.absPathKey = filekey.name
        except:
            self.keyBtnText.set("Browse Key")
        else:
            nameFileKey = self.get_name(self.absPathKey)
            self.lblKey.configure(text=nameFileKey)
            self.keyBtnText.set("Browse Key")
            
            self.openTVBtn()

    def find_database(self):
        self.fileBrowseText.set("Browse ...")
        try :
            filekey = filedialog.askopenfile(title="Select Database",filetypes=[("Crypted sqlite3 file","*.dbc"),("All Types", "*")])
            self.absPathdatabase = filekey.name
        except:
            self.fileBrowseText.set("Browse Database")
        else:
            nameFileDatabase = self.get_name(self.absPathdatabase)
            self.lblBrowse.configure(text=nameFileDatabase)
            self.fileBrowseText.set("Browse Database")
            
            self.openTVBtn()

    def afterBtnOpen(self):

        filekey = open(self.absPathKey, 'rb')
        self.key = filekey.read()
        filekey.close()
        try:
            fer = Fernet(self.key)
        except:
            messagebox.showinfo('Something Wrong','have problems with the key \nprobably not the good ones')
            self.querryDataBase()
        else:
            tempFiledecrypt = open(self.absPathdatabase, 'rb')
            try:
                DbDecrypt = tempFiledecrypt.read()
            except:
                tempFiledecrypt.close()
                self.querryDataBase()
            else:
                #self.pathTFileDCrypt = tempFiledecrypt.name
                tempFiledecrypt.close()
                try:
                    DcryptContent = fer.decrypt(DbDecrypt)
                except:
                    print('ici')
                else:
                    nameFile = self.get_name(self.absPathdatabase)
                    for k in range(0,4):
                        nameFile = nameFile[:-1]
                    fileDbDcrypt = open(TempFileDc, 'wb')
                    self.absTempDb = fileDbDcrypt.name
                    fileDbDcrypt.write(DcryptContent)
                    self.absDCPathdatabase = fileDbDcrypt.name
                    #print(self.absDCPathdatabase)
                    fileDbDcrypt.close()
                    self.querryDataBase()

    def cryptDbFile(self):
        try:
            fer = Fernet(self.key)
        except:
            messagebox.showinfo('Something Wrong','have problems with the key \ngo on menu bar folder \nand generate file key')
        else:
            tempFileCrypt = open(self.absDCPathdatabase, 'rb')
            DbCrypt = tempFileCrypt.read()
            tempFileCrypt.close()

            CryptContent = fer.encrypt(DbCrypt)

            try:
                fileCrypt = filedialog.asksaveasfile(title="Save your Crypted Database", filetypes=[("Crypted Database",".dbc")], initialfile=('Protected database'), defaultextension=".dbc")
                
            except:
                print("Erreur Crypt")
            else:
                try:
                    TFileCrypt = open(fileCrypt.name, 'wb')
                except:
                    pass
                else:
                    TFileCrypt.write(CryptContent)
                    
                    TFileCrypt.close()
                    #print("1 =",self.absPathdatabase, "2 =", self.absPathdatabase)
                    remove(self.absPathdatabase)
                    #print(self.pathTFileDCrypt)
                    remove(self.absDCPathdatabase)
                    self.querryDataBase()
    
    def SavageClose(self):
        try:
            remove(self.absDCPathdatabase)
        except:
            pass


# other fonction for create key with password in menubar
    def gen_key_by_password(self,password):
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

    def afterKfile(self,e):
            password = self.entrypswd.get()
            lenPswd = len(password)
            if lenPswd <= 7:
                self.labelEntry2.configure(text='min 8 lenght')
            elif lenPswd > 7:
                self.labelEntry2.configure(text='Ok')

                key = self.gen_key_by_password(password)
                
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

    def CheckGenerate(self, e):
        size = self.entrySize.get()      
        if size.isdigit() == True:
            size = int(size)
            if size > 7:
                self.lblSizeLeft.configure(text='Ok')              
                password = random_password1(size)

                self.TxtBoxPswd.delete(1.0, "end")
                self.TxtBoxPswd.insert(1.0, password)

            elif size <= 7:
                k = 8   - size
                self.lblSizeLeft.configure(text=f'adds min {k}')
            elif size > 90:
                self.lblSizeLeft.configure(text="Max 90")
        else:
            self.lblSizeLeft.configure(text='number only')

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

l = 0
