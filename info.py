from pymongo import  MongoClient

def datos_falsos(nombre_db,nombre_coleccion):
	client = MongoClient("localhost",27017)
	db =client[nombre_db]
	col = db[nombre_coleccion]


	col.insert_many([{
	"ID" : "0",
	"fecha_grabacion" : "04/09/1999",
	"ciudad" : "Valdivia",
	"duracion":"00:20",
	"latitud" : -39.81435313,
	"longitud": -73.24562389,
	"ubicacion": "interior",
	"usuario":{
		"Nombre": "Cata",
		"Apellido" : "Martin",
		"rut" : "112222111-1"
	},
	"segmentos": [{
		"ID": "id0",
		"categoria" : "Musica",
		"formato" : "wav",
		"duracion" : "00:10", 
		"inicio" : "00:05", 
	    "fin" : "00:15",
		"etiquetas" : [{ 
		"nombre_fuente" : "violin", 
		"descripcion" : "artista",
		"id_analizador" : "0"
		}
		]
	}	
	]},{"ID" : "1",
	"fecha_grabacion" : "03/02/1999",
	"ciudad" : "Valdivia",
	"duracion":"00:20",
	"latitud" : -39.843213,
	"longitud": -73.2432439,
	"ubicacion": "exterior",
	"usuario":{
		"Nombre": "lina",
		"Apellido" : "San",
		"rut" : "13264111-1"
	},
	"segmentos": [{
		"ID": "id0",
		"categoria" : "Animales",
		"formato" : "wav",
		"duracion" : "00:10", 
		"inicio" : "00:05", 
	    "fin" : "00:15",
		"etiquetas" : [{ 
		"nombre_fuente" : "vaca", 
		"descripcion" : "mugido",
		"id_analizador" : "0"
		}
		]
	}	
	]},{"ID" : "2",
	"fecha_grabacion" : "03/09/2000",
	"ciudad" : "Valdivia",
	"duracion":"00:20",
	"latitud" : -39.84235313,
	"longitud": -73.24532679,
	"ubicacion": "interior",
	"usuario":{
		"Nombre": "Catalina",
		"Apellido" : "San Martin",
		"rut" : "111t42651-1"
	},
	"segmentos": [{
		"ID": "id0",
		"categoria" : "Climáticos y Medio ambientaless",
		"formato" : "wav",
		"duracion" : "00:10", 
		"inicio" : "00:05", 
	    "fin" : "00:15",
		"etiquetas" : [{ 
		"nombre_fuente" : "lluvia", 
		"descripcion" : "mucha lluvia",
		"id_analizador" : "0"
		}
		]
	}	
	]},{"ID" : "3",
	"fecha_grabacion" : "03/09/2009",
	"ciudad" : "Valdivia",
	"duracion":"00:20",
	"latitud" : -39.8234313,
	"longitud": -73.2786989,
	"ubicacion": "exterior",
	"usuario":{
		"Nombre": "Katalina",
		"Apellido" : "San_Martin",
		"rut" : "114575811-1"
	},
	"segmentos": [{
		"ID": "id0",
		"categoria" : "Mecánicos",
		"formato" : "wav",
		"duracion" : "00:10", 
		"inicio" : "00:05", 
	    "fin" : "00:15",
		"etiquetas" : [{ 
		"nombre_fuente" : "sierra", 
		"descripcion" : "talar madera",
		"id_analizador" : "0"
		}
		]
	}	
	]},{"ID" : "4",
	"fecha_grabacion" : "03/09/2019",
	"ciudad" : "Valdivia",
	"duracion":"00:20",
	"latitud" : -38.8121313,
	"longitud": -72.24589,
	"ubicacion": "interior",
	"usuario":{
		"Nombre": "talina",
		"Apellido" : "Martin",
		"rut" : "11231234111-1"
	},
	"segmentos": [{
		"ID": "id0",
		"categoria" : "Vehiculos",
		"formato" : "wav",
		"duracion" : "00:10", 
		"inicio" : "00:05", 
	    "fin" : "00:15",
		"etiquetas" : [{ 
		"nombre_fuente" : "auto", 
		"descripcion" : "choque",
		"id_analizador" : "0"
		}
		]
	}	
	] },{"ID" : "0",
	"fecha_grabacion" : "03/09/1999",
	"ciudad" : "Valdivia",
	"duracion":"00:20",
	"latitud" : -39.8121313,
	"longitud": -73.24589,
	"ubicacion": "interior",
	"usuario":{
		"Nombre": "Catalina",
		"Apellido" : "San Martin",
		"rut" : "11111111-1"
	},
	"segmentos": [{
		"ID": "id0",
		"categoria" : "Humanos",
		"formato" : "wav",
		"duracion" : "00:10", 
		"inicio" : "00:05", 
	    "fin" : "00:15",
		"etiquetas" : [{ 
		"nombre_fuente" : "bebe", 
		"descripcion" : "llanto de un bebe",
		"id_analizador" : "0"
		}
		]
	}	
	]} ] )