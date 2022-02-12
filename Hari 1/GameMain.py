import tkinter


kota1 = 'Mojokerto'
kota2 = 'Jember'
bensin = 40
batasMuatan = 200

#Declare Rute
Rute = ['Sidoarjo','Pasuruan','Probolinggo', 'Lumajang', 'Jember']
RuteJob = ['Sidoarjo Probolinggo','Probolinggo Jember']
BebanJob = [25,30]
#+-+-+-+-+-+-+

#Declare Jarak
totalJarak = 0
for i in range(1, len(Rute)):
    totalJarak = totalJarak + 200
#+-+-+--+-+-+-+


#Declare beban
totalBeban = 0
for a in range(1 , len(RuteJob)):
    totalBeban = totalBeban + BebanJob[a]

#Declare Bengsin
totalBensin = totalJarak / 20
#+++

#Main Algorithm
def Check():
    if totalBensin > bensin:
        print('Gagal')
        return
    
    #if rute.biaya == notStonk:
    #   print('Bobrok!')
    #   return
    
    if totalBeban > batasMuatan:
        print('Gagal')
        return
    
    #Declare Moving image
#   for n in Rute:
#       ImageTruk.animate from Rute[n] to Rute[n+1]
#       tk.Label['text'] = f'Truk sedang berjalan dari {Rute[n]} menuju {Rute[n+1]}, mengangkut muatan {id_muatan}'

#   tkinter.messagebox = 'Perjalanan Selesai, total uang yang didapatkan = {rute.biaya}'
#   tkinter.buttonCobaLagi()

#tkinter.buttonCobaLagi():
#   tk.OKCancelMessage('', 'Coba Lagi?', command={Yes, No})


