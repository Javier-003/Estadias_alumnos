from pymongo import MongoClient

MONGO_URI = 'mongodb+srv://equipo:YCPoxTsZv3Lr6N95@cluster0.kigg6os.mongodb.net/?retryWrites=true&w=majority'


def dbConnection():
    try:
        client = MongoClient(MONGO_URI)
        db = client["Universidad_Estadias"]
        
        return db
    except Exception as e:
        print('Error de conexión con la BD:', e)
        return None
