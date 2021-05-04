import flask
import mysql.connector
import sys
import json
from flask import jsonify
from flask_mysqldb import MySQL
from flask import render_template
from flask import request
import simplejson as json
import random

app = flask.Flask(__name__)

@app.route('/TestVerisiOlustur', methods = ['POST'])
def TestVerisiOlustur():
	
	try:
		ada_db = mysql.connector.connect(host="localhost", user="root", passwd="mertak5656M.", database="ada")
	except:
		sys.exit("Error connecting to the database. Please check your inputs.")
	db_cursor = ada_db.cursor(buffered=True)
	strings = ["Ankara", "İstanbul", "İzmir", "Bursa", "Edirne", "Konya", "Antalya", "Diyarbakır", "Van", "Rize"]
		
	msg_received = flask.request.get_json()
	musteriAdet = msg_received["musteriAdet"]
	sepetAdet = msg_received["sepetAdet"]
	for x in range(0, musteriAdet):
		Ad = "Mert"
		Soyad = "Ak"
		random_number = random.randint(0, 9)
		Sehir = strings[random_number]
		insert_query = "INSERT INTO musteri (Ad,Soyad,Sehir) VALUES (%s,%s,%s)"
		insert_values = (Ad,Soyad,Sehir)
		try:
			db_cursor.execute(insert_query, insert_values)
			ada_db.commit()
        
		except Exception as e:
			print("Error while inserting the new record :", repr(e))
	for x in range(0, sepetAdet):
		db_cursor.execute("SELECT COUNT(Id) FROM musteri")
		record2 = db_cursor.fetchone()
		musterisayisi = str(record2)
		musterisayisi = musterisayisi.strip('()')
		musterisayisi = musterisayisi.replace(',', '')
		int_musterisayisi = int(musterisayisi)
		random_number2 = random.randint(1, 5)
		random_musteri = random.randint(0,int_musterisayisi)
		
		insert_query = "INSERT INTO sepet (MusteriId) VALUES (%s)"
		insert_values = (random_musteri,)
		try:
			db_cursor.execute(insert_query, insert_values)
			ada_db.commit()
			
        
		except Exception as e:
			print("Error while inserting the new record :", repr(e))
			return "hata1"
		for y in range(1, random_number2+1):
			db_cursor.execute("SELECT MAX(Id) FROM sepet")
			record = db_cursor.fetchone()
			lastId = str(record)
			lastId = lastId.strip('()')
			lastId = lastId.replace(',', '')
			Aciklama = "Aciklama"
			
			random_numberTutar = random.randrange(100, 1000)
			insert_query2 = "INSERT INTO sepeturun (SepetId,Tutar,Aciklama) VALUES (%s,%s,%s)"
			insert_values2 = (lastId,random_numberTutar,Aciklama)
			try:
				db_cursor.execute(insert_query2, insert_values2)
				ada_db.commit()
        
			except Exception as e:
				print("Error while inserting the new record :", repr(e))
				return "hata2"

	
	

	return "tamam"
	
@app.route('/SehirBazliAnalizYap', methods = ['POST','GET'])
def SehirBazliAnalizYap():
	result =[
	]
	a = []
	sepetsayisi = [0 for x in range(10)]
	sehrintutari = [0 for x in range(10)]
	
	strings = ["Ankara", "İstanbul", "İzmir", "Bursa", "Edirne", "Konya", "Antalya", "Diyarbakır", "Van", "Rize"]
	
	for x in range(0, 10):
		Sehir = strings[x]
		db_cursor.execute("SELECT COUNT(musteri.Id) as number  FROM musteri,sepet where musteri.Id = sepet.MusteriId AND Sehir = " + "'" + Sehir + "'") 
		record = db_cursor.fetchone()
		sepetsayi = str(record)
		sepetsayi = sepetsayi.strip('()')
		sepetsayi = sepetsayi.replace(',', '')
		
		
		
		
		tutar = 0
		db_cursor.execute("SELECT (sepet.Id)   FROM musteri,sepet where musteri.Id = sepet.MusteriId AND Sehir = " + "'" + Sehir + "'") 
		
		for row in db_cursor.fetchall():
			count = row[0]
			db_cursor.execute("SELECT SUM(Tutar) as toplam   FROM sepeturun where SepetId =  " + str(count))
			record2 = db_cursor.fetchone()
			toplamtutar = str(record2)
			toplamtutar = toplamtutar.strip('()')
			toplamtutar = toplamtutar.replace(',', '')
			
			if toplamtutar == "None":
				record2 = db_cursor.fetchone()
				
			else:
				toplamtutar = toplamtutar.strip('()')
				toplamtutar = toplamtutar.replace('Decimal', '')
				toplamtutar = toplamtutar.strip('(')
				toplamtutar = toplamtutar.replace("'", "")
				tutar += int(toplamtutar)
			
			
		
		

		sepetsayisi[x] = sepetsayi
		sehrintutari[x] = tutar
		#result.append({'SehirAdi':Sehir, 'SepetAdet':sepetsayi, 'Tutar': tutar})
		
		
	#sıralama 
	eklenenler = [9999999999 for x in range(10)]
	
	maxindex = sehrintutari.index(max(sehrintutari))
	result.append({'SehirAdi':strings[maxindex], 'SepetAdet':sepetsayisi[maxindex], 'Tutar': sehrintutari[maxindex]})
	eklenenler[maxindex] = maxindex

	
	
	for z in range(0, 9):
		#maxindex = sehrintutari.index(min(sehrintutari))
		#maks = min(sehrintutari)
		for x in range(0,10):
			if(eklenenler[x] == 9999999999):
				maxindex = x
				maks = sehrintutari[x]
		for x in range(0,10):
			if(maks < sehrintutari[x]):
				checker = True
				for y in range(0,10):
					if(x == eklenenler[y]):
						checker = False
				if checker:
					maxindex = x
					maks = sehrintutari[x]
					
					
		
		result.append({'SehirAdi':strings[maxindex], 'SepetAdet':sepetsayisi[maxindex], 'Tutar': maks})
		eklenenler[maxindex] = maxindex
	 
	
	return jsonify(result)
	
	


try:
    ada_db = mysql.connector.connect(host="localhost", user="root", passwd="mertak5656M.", database="ada")
except:
    sys.exit("Error connecting to the database. Please check your inputs.")
db_cursor = ada_db.cursor(buffered=True)
if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)