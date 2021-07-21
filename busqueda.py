import folium
from pymongo import  MongoClient
from folium.plugins import MarkerCluster
from info import datos_falsos
import subprocess

def play(audio_file_path):
    subprocess.call(["ffplay", "-nodisp", "-autoexit", audio_file_path])

def pedir_ruta():
	class E (Exception):
		pass
	class vacio (E):
		pass
	class malIngresada (E):
		pass
	class solocomas (E):
		pass
	while True:
		try:
			nombre = input("Ingrese la ruta de su archivo .wav (si esta en la misma carpeta, solo el nombre):\n")
			if len(nombre)==0:
				raise vacio
			elif len(nombre.replace(" ",""))==0:
				raise solocomas
			archivo = open (nombre,"rb")
			if (nombre.split(".")[-1]=="wav"):
				archivo.close()
				return nombre
			else:
				raise malIngresada
		except malIngresada:
			print("Error, al parecer lo ingresaste mal. Vuelve a Intentar")
		except vacio:
			print("Error, no ingresaste nada. Vuelve a Intentar")
		except solocomas:
			print("Error, ingresaste solo espacios. Vuelve a Intentar")
		except FileNotFoundError:
			print('Error, Archivo no encontrado, asegurate de haberlo escrito bien \nEj: "/home/name_usuario/Escritorio/ejemplo.wav"')

def desplegar_bases(lista):
	for i in range(0,len(lista)):
		print("{}.{}".format(i+1,lista[i]),end=" ")
	print()

def validar_dia(x): # True si esta mal ingresado, False sino
	a = x.split("/")
	dia = a[0]
	mes = a[1]
	year= a[2]

	if (not dia.isnumeric() or not mes.isnumeric() or not year.isnumeric()):
		return True
	dia = int(dia)
	mes = int(mes)
	year = int(year)

	if ((dia<0 or dia>31) or (mes<0 or mes>12) or (year>2021 or year<1900)):
		return True
	return False

def preguntar_busqueda(): #Pregunta que buscara
	buscar=input("¿Qué buscará?: \n1. Por día de creación: \n2. Por una categoria: \n")
	while not(verificar_preguntar(buscar)):
		print('Error!!, solo puede ingresar "1" o "2"')
		buscar=input("¿Qué buscará?: \n1. Por día de creación: \n2. Por una categoria: \n")
	return buscar.replace(" ","")

def verificar_preguntar(text): #valida que se ingreso bien la pregunta
	x=text.replace(" ","")
	if len(text)==0 or len(x)!=1:
		return False
	elif x=="1" or x=="2":
		return True

def mapa(): #pide la categoria (1 o 2) TIENE UNA FUNCION "DATOS_FALSOS()" QUE INGRESARÁ 30 DATOS A LA BASE DE DATOS ESCOGIDA
	client = MongoClient("localhost",27017)
	
	print("Estas son sus bases de datos: ")
	desplegar_bases(client.list_database_names())
	base = input("¿A cuál desea agregar?: ")
	while not(base in client.list_database_names()):
		print("#############################")
		print("Lo siento, esa base no existe")
		print("Estas son sus bases de datos: ")
		desplegar_bases(client.list_database_names())
		base = input("¿A cuál desea agregar?: ")
	db=client[base]
	
	print("Estas son sus colecciones disponibles:")
	desplegar_bases(db.list_collection_names())
	nombreColeccion = input("¿A cuál desea agregar?: ")
	while not(nombreColeccion in db.list_collection_names()):
		print("#############################")
		print("Lo siento, esa coleccion no existe")
		print("Estas son sus colecciones disponibles: ")
		desplegar_bases(db.list_collection_names())
		nombreColeccion = input("¿A cuál desea agregar?: ")
	col= db[nombreColeccion]

	for i in range(0,5):
		datos_falsos(base, nombreColeccion) #ingresa datos "inventados" en la base de datos
	
	x = preguntar_busqueda()
	mapa = folium.Map(location =[-39.81422,-73.24589 ], zoom_start= 12, control_scale= True)
	mc = MarkerCluster()
	if x == "1":
		i= int(x)-1
		dia_pedido = pedir_dia()
		for info in col.find({"fecha_grabacion":dia_pedido}):
			latitud = info["latitud"]
			locacion = info["longitud"]
			categoria = info["segmentos"][0]["categoria"]
			mc.add_child(folium.Marker(location = [latitud,locacion], popup=categoria))
	else:
		categoria_busqueda = pedir_categoria()
		for info in col.find({"segmentos" : {"$elemMatch" : {"categoria":categoria_busqueda} } }):
			latitud = info["latitud"]
			locacion = info["longitud"]
			fecha = info["fecha_grabacion"]
			mc.add_child(folium.Marker(location = [latitud,locacion], popup=fecha))
	mapa.add_child(mc)
	nombre_mapa = "mapa_"+base+".html"
	mapa.save(nombre_mapa)

def pedir_dia():
	dia = input("Ingrese Fecha de grabación: \ndd/mm/aaaa\n")
	while (validar_dia(dia)):
		print("Error!!, Vuelva a intentar. Ej: 15/11/1999")
		dia = input("Ingrese Fecha de grabación: \ndd/mm/aaaa\n")
	return dia

def pedir_categoria():
	cat = ["Humanos","Musica","Animales","Climáticos y medio ambientales","Mecánicos","Vehiculos", "Alertas"]
	text = categoria="¿Qué categoria buscará?: \n1- Humanos (habla, grita, etc.)\n2- Música\n3- Animales\n4- Climáticos y Medio ambientales (lluvia, viento, etc.)\n5- Mecánicos (motosierra, explosión, etc.\n6- Vehiculos\n7- Alertas (Sirena, bocina, etc.)\n"
	categoria=input(text)
	while not(verificar_categoria(categoria)):
		print('Error!!, solo puede ingresar "1", "2", "3", "4", "5", "6" o "7" ')
		categoria=input(text)
	elec = int(categoria.replace(" ",""))-1
	return cat[elec]

def verificar_categoria(text): #True si la categoria elegida existe
	num= "1234567"
	x=text.replace(" ","")
	if len(text)==0 or len(x)!=1:
		return False
	elif (x in num):
		return True

def respuesta_audio(respuesta):
	if respuesta.lower() == "si":
		nombre_archivo = pedir_ruta()
		play(nombre_archivo)

def main():
	mapa()
	respuesta = input("¿Quiere reproducir un audio.wav?: Si , No: \n")
	respuesta_audio(respuesta)
	
main()
