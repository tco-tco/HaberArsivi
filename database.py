import mysql.connector
import pandas.io.sql as sql
from userInfo import host, user, password
#from asyncio.windows_events import NULL 

def createDB(dbName):
    connection=mysql.connector.connect(host=host, user= user, password=password)
    cursor=connection.cursor()
    cursor.execute(f"CREATE DATABASE {dbName}")
def createTable(ilAdi,dbName):
    connection=mysql.connector.connect(host=host, user= user, password=password, database=f"{dbName}")
    cursor=connection.cursor()

    cursor.execute(f"CREATE TABLE {ilAdi} (ID INT PRIMARY KEY AUTO_INCREMENT, Haber_Baslıgı VARCHAR(250), Haber_Tarihi VARCHAR(15), Gösterim_Sayısı INT(4), Haber_Text MEDIUMTEXT, URL MEDIUMTEXT, Haber_URL_No INT(4), IMG_URL MEDIUMTEXT, Hata VARCHAR(25))") #kayıt eklemek için kullanılır

def insertValue(ilAdi, Haber_Baslıgı, Haber_Tarihi, Gösterim_Sayısı, Haber_Text, URL, Haber_URL_No, IMG_URL, Hata,dbName):
    connection=mysql.connector.connect(host=host, user= user, password=password, database=f"{dbName}")
    cursor=connection.cursor()

    sql=f"INSERT INTO {ilAdi} (Haber_Baslıgı, Haber_Tarihi, Gösterim_Sayısı, Haber_Text, URL, Haber_URL_No, IMG_URL, Hata) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"   # Products: tablo adı, parantez içine kolonların adını giriyoruz, VALUES parantez içinde ise değerler kolon sırasına uygun olarak girilir(%s'ler yer tutucu görevinde)
                                                                                       # Nullable eğer NO ise mutlaka değer girilmelii değilse tüm kolonların adını vermeye gerek olmadan işlem yapılabilir
    values=(Haber_Baslıgı, Haber_Tarihi, Gösterim_Sayısı, Haber_Text, URL, Haber_URL_No, IMG_URL, Hata)

    # Haber_Baslıgı, Haber_Tarihi, Gösterim_Sayısı, Haber_Text, URL, Haber_URL_No, Hata
    #     title        date             pageView      text      url     haberNo    hata

    cursor.execute(sql,values)

    try:
        connection.commit()
        #print(f"{cursor.rowcount} tane kayıt eklendi")
        print(f"son eklenen kayıt id: {cursor.lastrowid}")
    except mysql.connector.Error as err:
        print("hata: ", err)

    # finally:
    #     connection.close()
    #     print("database bağlantısı kapandı")


def insertValues(ilAdi,list,dbName):
    connection=mysql.connector.connect(host=host, user= user, password=password, database=f"{dbName}")
    cursor=connection.cursor()

    sql=f"INSERT INTO {ilAdi} (Haber_Baslıgı, Haber_Tarihi, Gösterim_Sayısı, Haber_Text, URL, Haber_URL_No, IMG_URL, Hata) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                                                                            
    values=list

    cursor.executemany(sql,values)  # birden fazla kayıt ekleneceği zaman execute yerine executemany kullanılır

    try:
        connection.commit()
        #print(f"{cursor.rowcount} tane kayıt eklendi")
        print(f"son eklenen kayıt id: {cursor.lastrowid}")
    except mysql.connector.Error as err:
        print("hata: ", err)

    # finally:
    #     connection.close()
    #     print("database bağlantısı kapandı")


