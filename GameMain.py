from functools import total_ordering
import math
import re
from matplotlib.pyplot import bar
import pandas as pd
from Graph import Jatim
import project

barang = pd.read_csv('dataset/Dataset-barang-angkut.csv')
kota = pd.read_csv('dataset/dataset_lat-long_jatim.csv', delimiter=';')

kota['Latitude'] = kota['Latitude'].astype('string').str.replace(',','.').astype('float64')
kota['Longitude'] = kota['Longitude'].astype('string').str.replace(',','.').astype('float64')

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
    
    if job1['JENIS'][0] == 'GAS' and job2['JENIS'][0] != 'GAS':
        try:
            job2 = jobList.loc[jobList['JENIS'] == 'GAS']
        except:
            pass
    
    if job1['JENIS'][0] == 'GAS' or job1['JENIS'][0] == 'CAIR':
        job1['BEBAN MUATAN (TON)'][0] = job1['BEBAN MUATAN (TON)'][0] + 4


    return job1



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
    if TotalBensin > int(project.entry.get()):
        project.labelhasilBensin['text'] = f'Bensin tidak cukup untuk menempuh rute manapun'
    else:
        project.labelhasilBensin['text'] = f'Total bensin yang dihabiskan {int(TotalBensin)} dari {project.entry.get()} liter'
    
    project.labelhasilRute['text'] = f'Rute terbaik yang dipilih adalah :\n{rute}'
    project.labelhasilJarak['text'] = f'Total jarak yang ditempuh : {int(Totaljarak)}Km'
    project.labelhasilJob['text'] = f'Muatan terbaik yang diambil :'

    reward = 0
    for i in range(0, len(jobs['ID'])):
        reward = reward + int(jobs['REWARD'][i])
    
    project.labelhasilJob['text'] = f'Total uang yang\nkita didapatkan : {reward}'
    
    
