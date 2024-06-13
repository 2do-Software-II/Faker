from pymongo import MongoClient
from faker import Faker
from bson.objectid import ObjectId
import random

# Reemplaza con tu URI de conexión a MongoDB Atlas
MONGO_URI = 'mongodb://mongo:iBebgtodjikVVRjkcYVaPJoShLURuLmY@roundhouse.proxy.rlwy.net:21591'

# Conectar a MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client['hotel']

# Colecciones
customers_collection = db['customer']
rooms_collection = db['room']
bookings_collection = db['booking']

# Crear instancia de Faker
fake = Faker('es_ES')

# Consultar todos los customers y rooms existentes
customers = list(customers_collection.find())
rooms = list(rooms_collection.find())

# Asegurarse de que hay customers y rooms disponibles
if not customers:
    raise ValueError("No hay customers disponibles en la colección 'customers'.")
if not rooms:
    raise ValueError("No hay rooms disponibles en la colección 'rooms'.")

# Función para generar un documento de booking falso con referencias a room y customer
def generar_reservacion_falsa():
    customer = random.choice(customers)
    room = random.choice(rooms)
    
    # Generar fechas y horas en el formato especificado
    date = fake.date_this_year().strftime("%d/%m/%Y")
    time = fake.time()
    start_date = fake.date_this_year().strftime("%d/%m/%Y")
    end_date = fake.date_this_year().strftime("%d/%m/%Y")
    
    # si el mes o el dia es de un solo digito aumentar un 0
    if len(start_date.split('/')[0]) == 1:
        start_date = '0' + start_date
    if len(start_date.split('/')[1]) == 1:
        start_date = start_date.split('/')[0] + '/0' + start_date.split('/')[1]

    return {
        'date': date,
        'time': time[:5],
        'status': fake.random_element(elements=('PENDIENTE', 'RESERVADO', 'CANCELADO','CHECKED_IN','FINALIZADO')),
        'checkIn': start_date,
        'checkOut': end_date,
        'prePaid': 0,
        'fullPayment': round(random.uniform(100.0, 3000.0), 2),
        'paymentMethod': fake.random_element(elements=('EFECTIVO', 'TARJETA', 'TRANSFERENCIA', 'DEPOSITO','ONLINE')),
        'startDate': start_date,
        'endDate': end_date,
        'room': {
            "$ref": "room",
            "$id": room['_id'],
            "$db": ""
        },
        'customer': {
            "$ref": "customer",
            "$id": customer['_id'],
            "$db": ""
        },
        '_class': 'com.okta.system.System.Entities.Booking'
    }

# Insertar documentos de booking en la colección
def poblar_base_de_datos(num_reservaciones):
    reservaciones = [generar_reservacion_falsa() for _ in range(num_reservaciones)]
    bookings_collection.insert_many(reservaciones)
    print(f'Se han insertado {num_reservaciones} reservaciones en la base de datos.')

# Número de documentos a insertar
NUMERO_DE_RESERVACIONES = 400

# Poblar la base de datos
poblar_base_de_datos(NUMERO_DE_RESERVACIONES)
