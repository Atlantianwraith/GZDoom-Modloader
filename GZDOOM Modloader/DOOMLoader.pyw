from tkinter import *
from tkinter import ttk
import sqlite3
import os
import sys

menu=Tk()
menu.title('DOOM Loader')
menu.iconbitmap('doom.ico')

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

def prof_add_btn():
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
        conn.commit
    conn.close

def prof_del_btn():
    sqlite3.connect('Doom.db')
    name = prof_input.get()
    if name:
        with sqlite3.connect('Doom.db') as conn:
            c = conn.cursor()
            c.execute('DELETE FROM profile WHERE prof = ?', (name,))
            if c.rowcount > 0:
                print('Profile {} has been deleted'.format(name))
                options = list(prof_input['values'])
                options.remove(name)
                prof_input['values'] = options
            else:
                print('Profile Doesn\'t Exist')
            prof_input.set('')
            conn.commit()
        conn.close

#DOOM Parameters
os.chdir('Source\\')
DOOM_mod=Listbox(menu, width=30)
DOOM2_mod=Listbox(menu, width=30)
doom='gzdoom -iwad \"iwad\\doom.wad\" -file \"..\\Doom1Mod\\'
doom2='gzdoom -iwad \"iwad\\doom2.wad\" -file \"..\\Doom2Mod\\'
save='\\*.*" -savedir "save\\'

#loading wads
modDir1=os.listdir('..\\Doom1Mod\\')
count1=1
for mod in modDir1:
    DOOM_mod.insert(count1, mod)
    count1+=1


modDir2=os.listdir('..\\Doom2Mod\\')
count2=1
for mod in modDir2:
    DOOM2_mod.insert(count2, mod)
    count2+=1


#functions to run doom
def doomLoad ():
    profile=prof_input.get()+'\\'
    mod1=DOOM_mod.get(ANCHOR)
    os.system(doom+mod1+save+profile+mod1)
    print(doom+mod1+save+profile+mod1)
    #sys.exit()

def doom2Load ():
    profile=prof_input.get()+'\\'
    mod2=DOOM2_mod.get(ANCHOR)
    #os.system(doom2+mod2+save+profile+mod2)
    print(doom2+mod2+save+profile+mod2)
    #sys.exit()

create_table()

DOOM_button=Button(menu, text='Load DOOM', width=10, command=doomLoad)
DOOM2_button=Button(menu, text='Load DOOM2', width=10, command=doom2Load)
prof_add_btn = Button(menu, text='Add', width=10, command=prof_add_btn)
prof_input = ttk.Combobox(menu, width=40)
prof_del_btn = Button(menu, text='Delete', width=10, command=prof_del_btn)

prof_input.grid(column=0, row=0, columnspan=2)
prof_add_btn.grid(column=0, row=1)
prof_del_btn.grid(column=1, row=1)
DOOM_mod.grid(column=0, row=2)
DOOM2_mod.grid(column=1, row=2)
DOOM_button.grid(column=0, row=3)
DOOM2_button.grid(column=1, row=3)

prof_input['values']=prof_value_input()

menu.mainloop()