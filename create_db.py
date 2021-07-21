from pymongo import  MongoClient

def pedir():
	rut = input("Ingrese Rut: ")
	while (not verificar_Rut(rut)):
		print("Error!!, Vuelva a intentar. Ej: 12345678-9 o 12.345.678-9")
		rut = input("Ingrese Rut: ")
	nombre = input("Ingrese su Nombre: ")
	while (not verificar_Nombre(nombre)):
		print("Error!!, Vuelva a intentar")
		nombre = input("Ingrese su Nombre: ")
	apellido = input("Ingrese su Apellido: ")
	while (not verificar_Nombre(apellido)):
		print("Error!!, Vuelva a intentar")
		apellido = input("Ingrese su Apellido: ")
	return [rut,sin_espacio(nombre),sin_espacio(apellido)]
def sin_espacio(text):
	x=text.split(" ")
	y=""
	for i in x:
		if(i!="" and i!=x[-1]):
			y+=i
			y+=" "
		else:
			y+=i
	return y
def verificar_Nombre(text):
	if len(text)==0 or len(text.replace(" ",""))==0:
		return False
	x=True
	for i in text:
		x = x and not(i.isnumeric())
	return x
def verificar_Rut(text):
	try:
		numero , digito = text.split("-")
		if (len(digito)!=1):
			return False
		x=True
		y=False
		for i in numero:
			x = x and (i.isnumeric() or i==".")
			if i == ".":
				y=True
		if y:
			sinp=numero.split(".")
			x=x and (len(sinp[1])==3) and (len(sinp[2])==3)
			rut=int("".join(sinp))
		else:
			rut=int(numero)
		return x and (rut>3000000)
	except ValueError:
		return False
def que_Hacer():
	hacer=input("¿Qué hará?: \n1. Crear Base de Datos: \n2. Agregar a la Base de Datos: \n")
	while not(verificar_Hacer(hacer)):
		print('Error!!, solo puede ingresar "1" o "2"')
		hacer=input("¿Qué hará?: \n1. Crear Base de Datos: \n2. Agregar a la Base de Datos: \n")
	return hacer.replace(" ","")
def verificar_Hacer(text):
	x=text.replace(" ","")
	if len(text)==0 or len(x)!=1:
		return False
	elif x=="1" or x=="2" or x=="3":
		return True

def desplegar_bases(lista):
	for i in range(0,len(lista)):
		print("{}.{}".format(i+1,lista[i]),end=" ")
	print()
def main():
	client = MongoClient("localhost",27017) #iniciar mongo
	respuesta = que_Hacer()
	if respuesta=="1":
		nombreDB=input("¿Cuál será el nombre de la base de datos?: ")
		db = client[nombreDB]
		nombreColeccion=input('¿Y el nombre de su colección para los "Usuarios"?: ')
		usu = db[nombreColeccion]
		y=pedir()
		a={"Rut": y[0],"Nombre": y[1][0].upper()+y[1][1:], "Apellido": y[2][0].upper()+y[2][1:]}
		usu.insert_one(a)
		print("Agregado con exito! :) ")
	else:
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
		usu= db[nombreColeccion]
		y=pedir()
		a={"Rut": y[0],"Nombre": y[1][0].upper()+y[1][1:], "Apellido": y[2][0].upper()+y[2][1:]}
		usu.insert_one(a)
		print("Agregado con exito! :) ")
	client.close()
main()