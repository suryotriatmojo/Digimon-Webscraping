# before run this program, you need to describe your password in line 34

from bs4 import BeautifulSoup
import requests
import csv
import mysql.connector

# web scraping digimon
url = 'https://wikimon.net/Visual_List_of_Digimon'
x = requests.get(url)
y = BeautifulSoup(x.content, 'html.parser')

list_nama = []
list_src = []
for a in y.find_all('img'):
    list_nama.append(a.get('alt'))
    list_src.append('https://wikimon.net'+a.get('src'))

row = []
n = 0
while n < len(list_nama)-2:
    row.append([list_nama[n], list_src[n]])
    n += 1

with open('digimon.csv', 'w') as data_digimon:
    writer = csv.writer(data_digimon)
    writer.writerows(row)

# insert csv file to sql
my_db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = '_________',        # you need to describe your password
    database = 'digimon'
    )

x = my_db.cursor()

# reset database index (delete then reset auto increment)
hapus = x.execute('delete from digimon')
mulai = x.execute('ALTER TABLE digimon AUTO_INCREMENT = 1')

csv_data = csv.reader(open('digimon.csv', 'r'))

for row in csv_data:
    x.execute('INSERT INTO digimon (nama,gambar) VALUES(%s, %s)',row)
    my_db.commit()
x.close()

# cara lain kalo mau masukin sql langsung tanpa akses csv
'''
for i in range(len(row)):
    nama = list_nama[i]
    gambar = list_src[i]
    x.execute('insert into digimon (nama, gambar) values (%s, %s)', (nama, gambar))
    my_db.commit()
'''