
#=========================== import library yang dibutuhkan ===========================
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import font
import math
import pandas as pd
from Graph import Jatim


#=========================== import dataset berupa csv menggunakan pandas ===========================
df = pd.read_csv('dataset/Dataset-barang-angkut.csv')
df1 = pd.read_csv('dataset/dataset_lat-long_jatim.csv', delimiter=';')

#=========================== membuat list daerah dari dataset yang telah disediakan ===========================
daerah = df1['Daerah'].unique().tolist()

#=========================== mengatur ukuran dari tampilan ===========================
window = tk.Tk()
window.minsize(width=1280, height=700)
window.geometry('1280x700')
window.title('Jatim Truck Simulator')

#=========================== mendeklarasi barang dan kota dari dataset ===========================
barang = pd.read_csv('dataset/Dataset-barang-angkut.csv')
kota = pd.read_csv('dataset/dataset_lat-long_jatim.csv', delimiter=';')

#=========================== melakukan data preprocessing atau data cleaning ===========================
kota['Latitude'] = kota['Latitude'].astype('string').str.replace(',','.').astype('float64')
kota['Longitude'] = kota['Longitude'].astype('string').str.replace(',','.').astype('float64')

#=========================== membuat fungsi dasar rute ===========================
def cekJalur(graph, asal, tujuan):
    queue = [[asal]]
    visited = set()

    while queue:
        jalur = queue.pop(0)
        state = jalur[-1]

        if state == tujuan:
            return jalur
        elif state not in visited:
            for cabang in graph.get(state, []):

                jalurAkhir = list(jalur)
                jalurAkhir.append(cabang)
                queue.append(jalurAkhir)
                
            visited.add(state)
        
        if len(queue) == 0:
            return 'Tidak Ditemukan'

#=========================== membuat fungsi dasar perhitungan jarak ===========================
def HitungJarak(asal, tujuan):
    # Deklarasi 
    # Hitung Jarak
    d1 = kota.loc[kota['Daerah'] == asal].reset_index(drop=True)
    d2 = kota.loc[kota['Daerah'] == tujuan].reset_index(drop=True)

    x1 = d1['Longitude'][0]
    x2 = d2['Longitude'][0]
    y1 = d1['Latitude'][0]
    y2 = d2['Latitude'][0]

    jarakAkhir = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    jarakAkhir = jarakAkhir * 100    
    return jarakAkhir

#=========================== membuat fungsi dasar perhitungan muatan terbaik ===========================
def MuatanTerbaik(asal, tujuan):
    jobList = barang.loc[(barang['INITIAL'].str.contains(asal)) & (barang['GOAL'].str.contains(tujuan))].reset_index(drop=True)
    if len(jobList['ID']) == 0:
        return 'Tidak Ada Job yang bisa didapat, silahkan pilih kota lain'

    job1 = jobList.loc[jobList['REWARD'] == jobList['REWARD'].max()].reset_index(drop=True)
    job2 = pd.DataFrame()
    try:
        job2 = jobList.loc[jobList['REWARD'] == jobList['REWARD'].max()][1].reset_index(drop=True)
        pass
    except:
        pass
    
    #if job1['JENIS'][0] == 'GAS' and job2['JENIS'][0] != 'GAS':
        #try:
        #    job2 = jobList.loc[jobList['JENIS'] == 'GAS']
        #except:
        #    pass
    
    if job1['JENIS'][0] == 'GAS' or job1['JENIS'][0] == 'CAIR':
        job1['BEBAN MUATAN (TON)'][0] = job1['BEBAN MUATAN (TON)'][0] + 4


    return job1

#=========================== membuat fungsi akhir dari fungsi fungsi sebelumnya ===========================
def Main(data, asal, tujuan):
    #Mencari Rute
    rute = cekJalur(data, asal, tujuan)

    #Cek Bensin
    Totaljarak = 0
    jobs = pd.DataFrame()

    for i in range(0, len(rute)-1):
        if i == len(rute)-1:
            break
        asalRute = rute[i]
        tujuanRute = rute[i+1]
        
        Totaljarak = Totaljarak + HitungJarak(asalRute, tujuanRute)

        jobs = pd.concat([jobs, MuatanTerbaik(asalRute, tujuanRute)])
    
    TotalBensin = Totaljarak / 20
    if TotalBensin > int(entry.get()):
        labelhasilBensin['text'] = f'Bensin tidak cukup untuk menempuh rute manapun'
    else:
        labelhasilBensin['text'] = f'Total bensin yang dihabiskan {int(TotalBensin)} dari {entry.get()} liter'
    
    labelhasilRute['text'] = f'Rute terbaik yang dipilih adalah :\n{rute}'
    labelhasilJarak['text'] = f'Total jarak yang ditempuh : {int(Totaljarak)}Km'
    
    reward = 0
    for i in range(0, len(jobs['ID'])):
        print(i)
        reward = reward + int(jobs['REWARD'][i])
    
    labelhasilJob['text'] = f'Total uang yang\nkita didapatkan : {reward}'
    
#=========================== fungsi peringatan untuk tampilan ===========================
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
    elif entry.get()  == '': #Jika batas muatan kosong
        messagebox.showwarning('Peringatan', 'Tolong Tentukan Solar')
        return
    elif entry2.get()  == '': #Jika batas muatan kosong
        messagebox.showwarning('Peringatan', 'Tolong Tentukan batas muatan')
        return
    
    try:
        int(entry.get())
    except:          
        entry.delete(0, tk.END)
        messagebox.showerror('Error','Nilai Bengsin harus angka!')
        return
    try:
        int(entry2.get())
    except:
        entry2.delete(0,tk.END)
        messagebox.showerror('Error','Nilai Muatan harus angka!')
        return
    #lanjut
    messagebox.showinfo('Game Started', 'Game telah Dimulai !!!')
    
    #job function
    Main(Jatim, cmbbox1.get(), cmbbox2.get())

#=========================== fungsi tombol ===========================
def StartGame():
    framem1.destroy()
    frame_open.destroy()
    messagebox.showinfo('Game Started', 'Pilih kota yang dituju 😁')

def showfull():
    btnview['state']='disabled'
    btnterr['state']='normal'
    frameimg.place_forget()
    frameimg2.place(relwidth=1, relheight=0.7, relx=0, rely=0.09)

def showline():
    btnterr['state']='disabled'
    btnview['state']='normal'
    frameimg2.place_forget()
    frameimg.place(relwidth=1, relheight=0.7, relx=0, rely=0.09)

#=========================== palet warna ===========================
birusmk = '#007acc'
abusli = '#3c3c3c'
abuvs = '#252526'  
mainblck = '#1e1e1e' 

#=========================== frame tampilan ===========================
frame1 = tk.Frame(window, bg=abusli)
frame1.place(relwidth=1, height=20, relx=0, rely=0)

frame2 = tk.Frame(window, bg=abuvs)
frame2.place(relheight=1, width=400, x=0, y=20)

frame3 = tk.Frame(window, bg='#272727')
frame3.place(relheight=1, width=800, x=300, y=20)

frame4 = tk.Frame(window, bg=abuvs)
frame4.place(relheight=1, width=400, x=1000, y=20)

frame_open = tk.Frame(window,bg=abuvs)
frame_open.place(relwidth=1, relheight=1, relx=0, rely=0)

frameWM = tk.Frame(window, bg=birusmk)
frameWM.place(relwidth=1, height=25, x=0, rely=1, anchor='sw')

#=========================== frame dari main menu ===========================
framem1 = tk.Frame(frame_open, bg=abusli )
framem1.place(height=300, width=300, relx=0.5, rely=0.5, anchor='center')

lblJudul = tk.Label(frame_open, fg='white', text='Jatim Truck Simulator', font=('Roboto', 40, font.BOLD), bg=abuvs)
lblJudul.place(relx=0.5, y=40, anchor='n')

lblm1 = tk.Label(framem1, fg='white', text='Welcome', font=('Roboto',20,font.BOLD), bg=abusli )
lblm1.place(relx=0.5, y=10, anchor='n')

tblopen = tk.Button(framem1, fg='white', text='Mulai Game', font=('Roboto',20,font.BOLD), bg=birusmk,
                    activebackground='white', activeforeground=abusli, command=lambda: StartGame())
tblopen.place(relx=0.5, rely=0.3, width=200, anchor='n')

tblexit1 = tk.Button(framem1, fg='white', text='Exit', font=('Roboto',20,font.BOLD), bg=birusmk,
                    activebackground='white', activeforeground=abusli, command=lambda: window.destroy())
tblexit1.place(relx=0.5, rely=0.7, width=200, anchor='n')

#=========================== frame 2 dan isinya ===========================

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

#=========================== frame 3 ===========================

frameimg = tk.Frame(frame3, bg='white')
frameimg.place(relwidth=1, relheight=0.7, relx=0, rely=0.09)

header = tk.LabelFrame(frame3, bg='#252526', bd=0)
header.place(relwidth=1, height=30, x=0, y=0)

tabs = tk.Frame(frame3, bg='#1e1e1e')
tabs.place(relwidth=100, relx=0, height=20, y=30)

btnview = tk.Button(tabs, text='Line', bg='#111111', bd=0, fg='white', activebackground='#252526', state='disabled', activeforeground='white',command= lambda : showfull())
btnview.place(x=0, y=0, relheight=1, width=100)

btnterr = tk.Button(tabs, text='Map', bg='#1e1e1e', bd=0, fg='white', activebackground='#252526', activeforeground='white', command= lambda : showline())
btnterr.place(x=100, y=0, relheight=1, width=100)  #==== sampe sini tabsnya
                            
labele = tk.Label(header, bg='#1e1e1e', fg='white', font=('Calibri', 12, font.BOLD), text='Route Truck')
labele.place(x=0, y=0, relheight=1, width=150)

#=========================== gambar map ===========================
from PIL import Image, ImageTk

canvas = tk.Canvas(frameimg)
canvas.place(relwidth=1, relheight=1, relx=0, rely=0)
img = ImageTk.PhotoImage(Image.open('Assets/Peta Jawa Timur.png'))
imageCanvas = canvas.create_image(0, 0, anchor='n', image=img)
titik = tk.Frame(canvas, bg='red')
titik.place(width=10, height=10, rely=0.5, relx=0.43, anchor='n')

frameimg2 = tk.Frame(frame3, bg='white')
frameimg2.place(relwidth=1, relheight=0.7, relx=0, rely=0.09)

canvas1 = tk.Canvas(frameimg2)
canvas1.place(relwidth=1, relheight=1, relx=0, rely=0)
img1 = ImageTk.PhotoImage(Image.open('Line.png'))
imageCanvas1 = canvas1.create_image(0, 0, anchor='n', image=img1)
titik1 = tk.Frame(canvas, bg='red')
titik1.place(width=10, height=10, rely=0.5, relx=0.43, anchor='n')


# img2 = ImageTk.PhotoImage(Image.open('Assets/Truk egh.png'))
# imageCanvas2 = canvas.create_image(0,0, anchor='n', image=img2)

#=========================== kontrol arrow pada map ===========================
def left(e):
    canvas.move(imageCanvas, 10, 0)
    canvas1.move(imageCanvas, 10, 0)

def right(e):
    canvas.move(imageCanvas, -10, 0)
    canvas1.move(imageCanvas, -10, 0)

def Up(e):
    canvas.move(imageCanvas, 0, 10)
    canvas1.move(imageCanvas, 0, 10)

def Down(e):
    canvas.move(imageCanvas, 0, -10)
    canvas1.move(imageCanvas, 0, -10)

def move(e):
    x1 = -7.263360277
    y1 = 112.7456592
    x2 = -7.446228375
    y2 = 112.7178012
    xsel = (x1-x2) *30
    ysel = (y2-y1) *30
    canvas.move(imageCanvas, xsel, ysel)
    print(xsel, ysel)

window.bind('<Left>', left)
window.bind('<Right>', right)
window.bind('<Up>', Up)
window.bind('<Down>', Down)
window.bind('<u>', move)


#=========================== frame 4 ===========================
prem4up = tk.Frame(frame4,bg='#2b2b2b')
prem4up.place(relwidth=0.8, relheight=0.39,rely=0.1, relx=0.01)

prem4dwn = tk.Frame(frame4, bg='#2b2b2b')
prem4dwn.place(relwidth=0.8, relheight=0.38,rely=0.5, relx=0.01)

lblketr = tk.Label(frame4, text='INFO :', bg=abuvs, font=('Roboto',10,font.BOLD), fg='white')
lblketr.place(x=30, y=40)

labelhasilRute = tk.Label(prem4up, text='', bg='#2b2b2b', font=('Roboto',10), fg='white')
labelhasilRute.place(x=10, y=20)

labelhasilJarak = tk.Label(prem4up, text='', bg='#2b2b2b', font=('Roboto',10), fg='white')
labelhasilJarak.place(x=10, y=100)

labelhasilBensin = tk.Label(prem4up, text='', bg='#2b2b2b', font=('Roboto',10), fg='white')
labelhasilBensin.place(x=10, y=150)

labelhasilJob = tk.Label(prem4dwn, text='', bg='#2b2b2b', font=('Roboto',10), fg='white')
labelhasilJob.place(x=10, y=20)

labelhasilReward = tk.Label(prem4dwn, text='', bg='#2b2b2b', font=('Roboto',10), fg='white')
labelhasilReward.place(x=10, y=150)

#=========================== frame 5 / watermark ===========================
watermark = tk.Label(frameWM, text='SMKN 1 Kediri | 😅☝', background=birusmk, font=('Calibri',11), fg='white')
watermark.place(x=10, rely=0.5, anchor='w')

#Map

#fig, ax = plt.
# peta = plt.imread('Assets/Peta Jawa Timur.png')
# plt.imshow(peta)
# tkplot = FigureCanvasTk(frame3, plt)
# tkplot.get_tk_widget().place(x=30, y=30)


window.mainloop()