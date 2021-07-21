from pymongo import  MongoClient
import gridfs
import wave
import contextlib

def pedir(text):
	class E (Exception):
		pass
	class vacio (E):
		pass
	class malIngresada (E):
		pass
	class soloEspacios (E):
		pass
	while True:
		try:
			nombre = input(text)
			if len(nombre)==0:
				raise vacio
			elif len(nombre.replace(" ",""))==0:
				raise soloEspacios
			elif text=="¿Fue grabado en el exterior o interior?: \n":
				if not(nombre.upper() == "INTERIOR" or nombre.upper() =="EXTERIOR"):
					raise malIngresada
				return nombre[0].upper()+nombre[1:].lower()
			elif text=="¿En que ciudad se grabo?\n":
				return nombre[0].upper()+nombre[1:].lower()
			return nombre

		except malIngresada:
			print("Error, al parecer lo ingresaste mal. Vuelve a Intentar")
		except vacio:
			print("Error, no ingresaste nada. Vuelve a Intentar")
		except soloEspacios:
			print("Error, ingresaste solo espacios. Vuelve a Intentar")

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

def conseguir_base_2(lista, respuesta):#ingreso un numero de la lista
	x = True
	for i in respuesta:
		x = x and (i.isnumeric())
	if x:
		if int(respuesta) <= len(lista) and int(respuesta) > 0:
			return x
	return False

def conseguir_base(client):
	print("Estas son sus bases de datos: ")
	lista_bases = client.list_database_names()
	desplegar_bases(lista_bases)	
	base = input("¿A cuál desea agregar el archivo .wav?: ")
	conse = conseguir_base_2(lista_bases,base)
	while not(base in lista_bases or conse):
		print("#############################")
		print("Lo siento, esa base no existe")
		print("Estas son sus bases de datos: ")
		desplegar_bases(lista_bases)
		base = input("¿A cuál desea agregar el archivo .wav?: ")
		conse = conseguir_base_2(lista_bases,base)
	if conse:
		return lista_bases[int(base)-1]
	return base

def duracion_audio(nombre):
	with contextlib.closing(wave.open(nombre,'r')) as f:
	    frames = f.getnframes()
	    rate = f.getframerate()
	    duration = frames / float(rate)
	return duration

def main():
	client = MongoClient("localhost",27017)
	base = conseguir_base(client)
	db =client[base]
	col = db["fs.files"]
	fs = gridfs.GridFS(db)
	nombre = pedir_ruta()
	fileID = fs.put(open (nombre,"rb"))
	fecha_grabacion = pedir("¿Cual fue la fecha de grabacion?\n")
	ciudad = pedir("¿En que ciudad se grabo?\n")
	latitud = pedir("Indique la latitud de la ubicacion:\n")
	longitud = pedir("Indique la longitud de la ubicacion:\n")
	exterior = pedir("¿Fue grabado en el exterior o interior?: \n")
	nombre_archivo = nombre.split("/")[-1]
	col.update_one({"_id":fileID},{
		"$set":{"filename":nombre_archivo,
				"duracion [s]":duracion_audio(nombre),
				"fecha_grabacion":fecha_grabacion, 
				"lugar":{"ciudad":ciudad,
				"exterior":exterior,
				"latitud":latitud,
				"longitud":longitud}
				}
			})
	client.close()
	print("Agregado con exito! :) ")

main()