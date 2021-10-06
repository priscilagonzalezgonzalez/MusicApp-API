import mysql.connector

#database connection
db = mysql.connector.connect(
    user='sarahi', password='12345678',
    database='musicapp')

#cursor
cursor = db.cursor()

def existe_usuario(correo):
    query = "SELECT COUNT(*) FROM usuario WHERE correo = %s"
    cursor.execute(query, (correo,))

    if cursor.fetchone()[0] == 1:
        return True
    else:
        return False

import hashlib
def crear_usuario(nombre, apellido, correo, contra):
    if existe_usuario(correo):
        return False
    else:
        h = hashlib.new('sha256', bytes(contra, 'utf-8'))
        h = h.hexdigest()
        insert_query = "INSERT INTO usuario(correo, contrasenia, nombre, apellido) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (correo, h, nombre, apellido))
        db.commit()

        return True

def iniciar_sesion(correo, contra):
    h = hashlib.new('sha256', bytes(contra, 'utf-8'))
    h = h.hexdigest()
    query = "SELECT id FROM usuario WHERE correo = %s AND contrasenia = %s"
    cursor.execute(query, (correo, h))
    id = cursor.fetchone()
    if id: #Si existe coincidencia
        return id[0], True
    else: 
        return None, False

def get_artista_id(nombre):
    query = "SELECT id FROM artista WHERE nombre = %s"
    cursor.execute(query, (nombre,))
    id = cursor.fetchone()
    if id: #Si existe coincidencia
        return id[0]
    else: 
        return None

def existe_artista(nombre):
    query = "SELECT COUNT(*) FROM artista WHERE nombre = %s"
    cursor.execute(query, (nombre,))

    if cursor.fetchone()[0] == 1:
        return True
    else:
        return False

def insertar_artista(nombre):
    insertar = "INSERT INTO artista(nombre) VALUES (%s)"
    cursor.execute(insertar, (nombre,))
    db.commit()

    if cursor.rowcount:
        return True
    else:
        return False


def existe_album(titulo, artista):
    query = "SELECT COUNT(*) FROM album WHERE titulo = %s AND artistaId = (SELECT id FROM artista WHERE nombre = %s)"
    cursor.execute(query, (titulo, artista))

    if cursor.fetchone()[0] == 1:
        return True
    else:
        return False

#Si no existe el artista, no existe el album
def insertar_album(album):
    titulo = album['titulo']
    anio = album['anio']
    imagen = album['imagen']
    usuarioId = album['usuarioId']
    nombre_artista = album['artista']

    #Validar si existe album
    if existe_album(titulo, nombre_artista):
        return False
    else:
        if existe_artista(nombre_artista):
            artista_id = get_artista_id(nombre_artista)
            insert_query = "INSERT INTO album (titulo, anio, imagen, usuarioId, artistaId) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (titulo, anio, imagen, usuarioId, artista_id))
            db.commit()

            if cursor.rowcount:
                return True
            else:
                return False
        else:
            if insertar_artista(nombre_artista):
                artista_id = get_artista_id(nombre_artista)
                insert_query = "INSERT INTO album (titulo, anio, imagen, usuarioId, artistaId) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(insert_query, (titulo, anio, imagen, usuarioId, artista_id))
                db.commit()

                if cursor.rowcount:
                    return True
                else:
                    return False
            else: #No se pudo insertar el artista, no se puede crear el album
                return False

def get_albums():
    query = "SELECT id, titulo, anio, imagen, usuarioId, artistaId FROM album"
    cursor.execute(query)
    albums = []
    for row in cursor.fetchall():
        album = {
            'id': row[0],
            'titulo': row[1],
            'anio': row[2],
            'imagen': row[3],
            'usuarioId': row[4],
            'artistaId': row[5]
        }
        albums.append(album)
    return albums





