from pymongo import MongoClient
from faker import Faker
from bson.objectid import ObjectId
import random

# Reemplaza con tu URI de conexión a MongoDB Atlas
MONGO_URI = 'mongodb://mongo:iBebgtodjikVVRjkcYVaPJoShLURuLmY@roundhouse.proxy.rlwy.net:21591'
abreviaturas_estados_bolivianos = ['LP', 'OR', 'PT', 'CQ', 'SC', 'CB', 'PA', 'CH', 'TA', 'BE']

# Conectar a MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client['hotel']

customers_collection = db['customer']
users_collection = db['User']
roles_collection = db['Role']

# Crear instancia de Faker
fake = Faker('es_ES')
# ID del role común para todos los usuarios
role_id = ObjectId('66661bb7ea87b472fcb66cde')

# Asegurarse de que el rol exista en la base de datos
roles_collection.update_one({'_id': role_id}, {'$setOnInsert': {'name': 'default_role'}}, upsert=True)

# Función para generar un documento de usuario falso
def generar_usuario_falso():
    return {
        'name': fake.user_name(),
        'password': fake.password(),
        'email': fake.email(),
        'role': {
            "$ref": "Role",
            "$id": role_id,
            "$db": ""
        },
        '_class': 'com.hotel.hotel.Entities.User'
    }

# Función para generar un documento de cliente falso con referencia a un usuario
def generar_cliente_falso(user_id):
    return {
        'name': fake.first_name(),
        'lastName': fake.last_name(),
        'phone': "+591 " + fake.numerify('7#######'),
        'address': fake.address(),
        'ci': fake.ssn(),
        'expedition': random.choice(abreviaturas_estados_bolivianos),
        'birthDate': fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat(),
        'nationality': fake.country(),
        'gender': fake.random_element(elements=('Masculino', 'Femenino')),
        'preference': fake.word(),
        'user': {
            "$ref": "User",
            "$id": user_id,
            "$db": ""
        },
        '_class': 'com.okta.system.System.Entities.Customer'
    }

# Insertar documentos en las colecciones
def poblar_base_de_datos(num_usuarios, num_clientes_por_usuario):
    # Insertar usuarios
    usuarios = [generar_usuario_falso() for _ in range(num_usuarios)]
    result = users_collection.insert_many(usuarios)
    user_ids = result.inserted_ids

    # Insertar clientes
    clientes = []
    for user_id in user_ids:
        for _ in range(num_clientes_por_usuario):
            clientes.append(generar_cliente_falso(user_id))
    
    customers_collection.insert_many(clientes)
    print(f'Se han insertado {num_usuarios} usuarios y {num_usuarios * num_clientes_por_usuario} clientes en la base de datos.')

# Número de documentos a insertar
NUMERO_DE_USUARIOS = 500
NUMERO_DE_CLIENTES_POR_USUARIO = 1

# Poblar la base de datos
poblar_base_de_datos(NUMERO_DE_USUARIOS, NUMERO_DE_CLIENTES_POR_USUARIO)