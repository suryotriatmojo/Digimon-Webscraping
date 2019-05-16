# before run this program, you need to describe your password in line 34

from bs4 import BeautifulSoup
import requests
import csv

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
import mysql.connector

my_db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = '________',        # you need to describe your password
    database = 'digimon'
    )

x = my_db.cursor()

for i in range(len(row)):
    nama = list_nama[i]
    gambar = list_src[i]
    x.execute('insert into digimon (nama, gambar) values (%s, %s)', (nama, gambar))
    my_db.commit()