from re import X
from turtle import width
import matplotlib.pyplot as plt
from matplotlib.pyplot import axis, text
import pandas as pd
#import tkinter gui
from cProfile import label
from ctypes import alignment
import tkinter as tk
from tkinter import Y, Frame, messagebox
from tkinter import ttk
from tkinter import font
from matplotlib.backends.backend_tkagg import FigureCanvasTk

df = pd.read_csv('dataset/Dataset-barang-angkut.csv')
df1 = pd.read_csv('dataset/dataset_lat-long_jatim.csv', delimiter=';')

daerah = df['INITIAL'].unique().tolist()

#
window = tk.Tk()
window.minsize(width=700, height=400)
window.geometry('1280x700')
window.title('Jatim Truck Simulator')

#gui

#Func

def Start():
    #Entry cek
    if cmbbox1.get() == '' or cmbbox2.get() == '':
        messagebox.showwarning('Peringatan', 'Tolong pilih Kota Awal dan Akhir')
        return
    elif cmbbox1.get() not in daerah:
        messagebox.showwarning('Peringatan', 'Kota Awal tidak masuk dalam daftar')
        cmbbox1.delete(0, tk.END)
        return
    elif cmbbox2.get() not in daerah:
        messagebox.showwarning('Peringatan', 'Kota Akhir tidak masuk dalam daftar')
        cmbbox2.delete(0, tk.END)
    elif cmbbox1.get() == cmbbox2.get():
        messagebox.showwarning('Peringatan', 'Kota tidak bisa sama')
        return
    elif entry.get() == '':
        messagebox.showwarning('Peringatan', 'Tolong tentukan jatah Solar')
        return
    # elif entry.get() is not int:
    #     messagebox.showwarning('Peringatan', 'Nilai Bensin harus integer')
    #     entry.delete(0, tk.END)
    #     return
    elif entry2.get()  == '': #Jika batas muatan kosong
        messagebox.showwarning('Peringatan', 'Tolong Tentukan batas muatan')
        return
    # elif entry2.get() is not int:
    #     messagebox.showwarning('Peringatan', 'Nilai Muatan harus integer')
    #     entry2.delete(0, tk.END)
    #     return
    
    messagebox.showinfo('Game Started', 'Game telah Dimulai !!!')
    
    job = df.loc[(df['INITIAL'] == cmbbox1.get()) & (df['GOAL'] == cmbbox2.get())]
    labelhasil['text'] = f'Job yang tersedia\n{job}'

    bebanMuatan = 'BEBAN MUATAN (TON)'
    job = job.loc[job['REWARD'] >= job['REWARD'].max()]
    
    Jenis = job['JENIS'].to_list()
    if Jenis[0] == 'CAIR' or Jenis[0] == 'GAS':
        job[bebanMuatan] = job[bebanMuatan] + 4

    labelhasil1['text'] = f'Rute terbaik : {job}'

def StartGame():
    framem1.destroy()
    frame_open.destroy()



#+-+-+-+-+-+-+-+-+-+-+-+-+-
birusmk = '#007acc'
abusli = '#3c3c3c'
abuvs = '#252526'  
mainblck = '#1e1e1e' 

#frame
frame1 = tk.Frame(window, bg=abusli)
frame1.place(relwidth=1, height=20, relx=0, rely=0)

frame2 = tk.Frame(window, bg=abuvs)
frame2.place(relheight=1, width=400, x=0, y=20)

frame3 = tk.Frame(window, bg=mainblck)
frame3.place(relheight=1, width=800, x=300, y=20)

frame4 = tk.Frame(window, bg=abuvs)
frame4.place(relheight=1, width=400, x=1000, y=20)

frame_open = tk.Frame(window,bg=abuvs)
frame_open.place(relwidth=1, relheight=1, relx=0, rely=0)

frameWM = tk.Frame(window, bg=birusmk)
frameWM.place(relwidth=1, height=25, x=0, rely=1, anchor='sw')

#entry

labelKA = tk.Label(frame2, text='KOTA AWAL', bg=abuvs, font=('Roboto',8,font.BOLD), fg='white')
labelKA.place(x=30, y=40)
cmbbox1 = ttk.Combobox(frame2)
cmbbox1['value'] = daerah
cmbbox1.place(x=30, y=60, width=200)

labelKA2 = tk.Label(frame2, text='KOTA AKHIR', bg=abuvs, font=('Roboto',8,font.BOLD), fg='white')
labelKA2.place(x=30, y=90)
cmbbox2 = ttk.Combobox(frame2)
cmbbox2['value'] = daerah
cmbbox2.place(x=30, y=120, width=200)

labelbs = tk.Label(frame2, text='SOLAR', bg=abuvs, font=('Roboto',8,font.BOLD), fg='white')
labelbs.place(x=30, y=150)
entry = tk.Entry(frame2)
entry.place(x=30, y=180 ,width=50)
labellt = tk.Label(frame2, text='liter', bg=abuvs, font=('Roboto',10), fg='white')
labellt.place(x=90, y=180)

labelmt = tk.Label(frame2, text='BATAS MUATAN', bg=abuvs, font=('Roboto',8,font.BOLD), fg='white')
labelmt.place(x=30, y=210)
entry2 = tk.Entry(frame2)
entry2.place(x=30, y=240, width=50)
labeltn = tk.Label(frame2, text='ton', bg=abuvs, font=('Roboto',10), fg='white')
labeltn.place(x=90, y=240)

tbl = tk.Button(frame2, text='MULAI', command=lambda: Start(), font=('Roboto',10, font.BOLD), bg=birusmk, foreground='white',activeforeground=birusmk)
tbl.place(x=30, y=280, width=220)

tblExit = tk.Button(frame2, text='EXIT', command=lambda: window.destroy(), font=('Roboto',10, font.BOLD), bg=birusmk,foreground='white',activeforeground=birusmk)
tblExit.place(x=30, rely=0.875, width=220)

#Map

#fig, ax = plt.
# peta = plt.imread('Assets/Peta Jawa Timur.png')
# plt.imshow(peta)
# tkplot = FigureCanvasTk(frame3, plt)
# tkplot.get_tk_widget().place(x=30, y=30)

#frame4
lblketr = tk.Label(frame4, text='INFO :', bg=abuvs, font=('Roboto',10,font.BOLD), fg='white')
lblketr.place(x=30, y=40)

labelhasil = tk.Label(frame4, text='', bg=abuvs, font=('Roboto',8), fg='white')
labelhasil.place(x=30, y=60)

labelhasil1 = tk.Label(frame4, text='', bg=abuvs, font=('Roboto',8), fg='white')
labelhasil1.place(x=30, y=90)

labelhasil2 = tk.Label(frame4, text='', bg=abuvs, font=('Roboto',8), fg='white')
labelhasil2.place(x=30, y=120)

#frm5
watermark = tk.Label(frameWM, text='SMKN 1 Kediri | 😅☝', background=birusmk, font=('Calibri',11), fg='white')
watermark.place(x=10, rely=0.5, anchor='w')

#frame main menu
framem1 = tk.Frame(frame_open, bg=abusli )
framem1.place(height=300, width=300, relx=0.5, rely=0.5, anchor='center')

lblm1 = tk.Label(framem1, fg='white', text='Login', font=('Roboto',20,font.BOLD), bg=abusli )
lblm1.place(relx=0.5, y=10, anchor='n')

tblopen = tk.Button(framem1, fg='white', text='Mulai Game', font=('Roboto',20,font.BOLD), bg=birusmk,
                    activebackground='white', activeforeground=abusli, command=lambda: StartGame())
tblopen.place(relx=0.5, rely=0.3, width=200, anchor='n')

tblexit1 = tk.Button(framem1, fg='white', text='Exit', font=('Roboto',20,font.BOLD), bg=birusmk,
                    activebackground='white', activeforeground=abusli, command=lambda: window.destroy())
tblexit1.place(relx=0.5, rely=0.7, width=200, anchor='n')

window.mainloop()