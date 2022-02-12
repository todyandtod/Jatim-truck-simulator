import pandas as pd
import matplotlib.pyplot as plt

kota = pd.read_csv('dataset_lat-long_jatim.csv', sep=';')

kota['Latitude'] = kota['Latitude'].astype('string').str.replace(',','.').astype('float64')
kota['Longitude'] = kota['Longitude'].astype('string').str.replace(',','.').astype('float64')

JalurSelatan = kota.reindex([19,11,9,7,4,23,26,30])
JalurPctSmnp = kota.reindex([19,16,5,22,20,29,10,24,27,0,31,15,18,12])
JalurNgTGK = kota.reindex([20,5,16,11])
JalurMdTgl = kota.reindex([5,21,6,9])
JalurBltMg = kota.reindex([7,6,8,4])
JalurKdrBjn = kota.reindex([6,25,3,29])
JalurNgjJb = kota.reindex([21,25])
JalurSbySd = kota.reindex([0,3,14])
JalurSbyJb = kota.reindex([0,14,17,1,13,28,26])
JalurMgLmj = kota.reindex([4,17,1,23])

plt.figure(figsize=(16,9))
plt.scatter(kota['Longitude'], kota['Latitude'], s=60)
plt.plot(JalurSelatan['Longitude'],JalurSelatan['Latitude'], '-r.')
plt.plot(JalurPctSmnp['Longitude'],JalurPctSmnp['Latitude'], '-r.')
plt.plot(JalurNgTGK['Longitude'],JalurNgTGK['Latitude'], '-r.')
plt.plot(JalurMdTgl['Longitude'],JalurMdTgl['Latitude'], '-r.')
plt.plot(JalurBltMg['Longitude'],JalurBltMg['Latitude'], '-r.')
plt.plot(JalurKdrBjn['Longitude'],JalurKdrBjn['Latitude'], '-r.')
plt.plot(JalurNgjJb['Longitude'],JalurNgjJb['Latitude'], '-r.')
plt.plot(JalurSbySd['Longitude'],JalurSbySd['Latitude'], '-r.')
plt.plot(JalurSbyJb['Longitude'],JalurSbyJb['Latitude'], '-r.')
plt.plot(JalurMgLmj['Longitude'],JalurMgLmj['Latitude'], '-r.')

plt.xticks([])
plt.yticks([])
# img = plt.imread('Assets/Peta Jawa Timur.png')
# plt.imshow(img)
plt.savefig('Line.png')
plt.show()