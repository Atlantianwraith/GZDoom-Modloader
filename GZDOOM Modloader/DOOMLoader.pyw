from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import os
import sys


menu=Tk()
menu.title('DOOM Loader')
menu.iconbitmap('doom.ico')

#DOOM Parameters
os.chdir('Source\\')
modDir=os.listdir('..\\Mods\\')
mapdir1=os.listdir('..\\Maps\\DOOM\\')
mapdir2=os.listdir('..\\Maps\\DOOM2\\')
doom='gzdoom -iwad \"iwad\\doom.wad\" -file \"..\\Mods\\'
doom2='gzdoom -iwad \"iwad\\doom2.wad\" -file \"..\\Mods\\'
mapd1='\\*.*\" \"..\\Maps\\DOOM\\'
mapd2='\\*.*\" \"..\\Maps\\DOOM2\\'
save=' -savedir "save\\'

iwaddir=os.listdir('iwad\\')
iwadvar=StringVar()
iwadvar.set(iwaddir[0])

def startup():
    create_table()
    popmapliststartup()
    prof_input['values']=prof_value_input()
    count=0
    for mod in modDir:
        modlist.insert(count, mod)
        count+=1

#DATABASE
def create_table():
    with sqlite3.connect('Doom.db') as conn:
        c=conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS profile ("prof" TEXT);')
        conn.commit()
    conn.close()

#Profile System
def prof_value_input():
    with sqlite3.connect('Doom.db') as conn:
        c=conn.cursor()
        c.execute('SELECT prof FROM profile')
        prof=[]
        for row in c.fetchall():
            prof.append(row[0])
        return prof
    conn.close()

def prof_add():
    name=prof_input.get()
    with sqlite3.connect('Doom.db') as conn:
        c=conn.cursor()
        c.execute('SELECT prof FROM profile')
        rows=c.fetchall()
        if (name,) in rows:
            print('Profile {} already exists'.format(name))
        else:
            c.execute('INSERT INTO profile VALUES (:prof)',{'prof':name})
            options = list(prof_input['values'])
            options.append(name)
            prof_input['values']=options
            print('Profile {} has been added'.format(name))
        conn.commit()
    conn.close()

def prof_del_btn():
    sqlite3.connect('Doom.db')
    name = prof_input.get()
    destroy = messagebox.askyesno('Remove Profile', 'Are you sure you would like to remove {}?\nThis will remove all of the profiles save data.'.format(name))
    if destroy == True:
        if name:
            with sqlite3.connect('Doom.db') as conn:
                c = conn.cursor()
                c.execute('DELETE FROM profile WHERE prof = ?', (name,))
                if c.rowcount > 0:
                    os.system('rmdir /s /q \"save\\{}\"'.format(name))
                    print('Profile {} has been deleted'.format(name))
                    options = list(prof_input['values'])
                    options.remove(name)
                    prof_input['values'] = options

                else:
                    print('Profile Doesn\'t Exist')
                prof_input.set('')
                conn.commit()
            conn.close()
    if destroy == False:
        return

def popmapliststartup():
    iwadvar.set(iwaddir[0])
    maplist.delete(0, END)
    count=0
    for imap in mapdir1:
        maplist.insert(count, imap)
        count+=1

def popmaplist(event):
    if 'DOOM.' in iwadvar.get():
        maplist.delete(0, END)
        count=0
        for imap in mapdir1:
            maplist.insert(count, imap)
            count+=1
    if 'DOOM2.' in iwadvar.get():
        maplist.delete(0, END)
        count=0
        for imap in mapdir2:
            maplist.insert(count, imap)
            count+=1

def loadGame():
    prof_add()
    profile=prof_input.get()+'\\'
    mod=modlist.get(ANCHOR)
    imap='\\'+maplist.get(ANCHOR)+'\"'
    if 'DOOM.' in iwadvar.get():
        os.system(doom+mod+mapd1+imap+save+profile+mod+imap)
        sys.exit()
        
    if 'DOOM2.' in iwadvar.get():
        os.system(doom2+mod+mapd2+imap+save+profile+mod+imap)
        sys.exit()
        

#Labels
iwadlab=Label(menu, text='IWAD:')
proflab=Label(menu, text='Profile:')
modlab=Label(menu, text='Mod List:')
maplab=Label(menu, text='Map List:')

maplist=Listbox(menu, width=30, exportselection=False)
modlist=Listbox(menu, width=30, exportselection=False)
game_button=Button(menu, text='Load DOOM', width=10, command=loadGame)
prof_add_btn = Button(menu, text='Add', width=10, command=prof_add)
prof_input = ttk.Combobox(menu, width=20)
prof_del_btn = Button(menu, text='Delete', width=10, command=prof_del_btn)
iwad_option = OptionMenu(menu, iwadvar, *iwaddir, command=popmaplist)

iwadlab.grid(row=0, column=0)
iwad_option.grid(row=0, column=1)
proflab.grid(row=1, column=0)
prof_input.grid(row=1, column=1)
prof_add_btn.grid(row=2, column=0)
prof_del_btn.grid(row=2, column=1)
modlab.grid(row=3, column=0)
maplab.grid(row=3, column=1)
modlist.grid(row=4, column=0)
maplist.grid(row=4, column=1)
game_button.grid(row=5, column=0)

startup()

menu.mainloop()
