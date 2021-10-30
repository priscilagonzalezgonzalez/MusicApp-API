import mysql.connector
import hashlib

#database connection
db = mysql.connector.connect(
    user='sarahi', password='12345678',
    database='musicapp')

#cursor
cursor = db.cursor()

class Usuarios:
    @classmethod
    def existe_usuario(self, correo):
        query = "SELECT COUNT(*) FROM usuario WHERE correo = %s"
        cursor.execute(query, (correo,))

        if cursor.fetchone()[0] == 1:
            return True
        else:
            return False

    @classmethod
    def crear_usuario(self, nombre, apellido, correo, contra):
        if self.existe_usuario(correo):
            return False
        else:
            h = hashlib.new('sha256', bytes(contra, 'utf-8'))
            h = h.hexdigest()
            insert_query = "INSERT INTO usuario(correo, contrasenia, nombre, apellido) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (correo, h, nombre, apellido))
            db.commit()
            return True

    @classmethod
    def iniciar_sesion(self, correo, contra):
        h = hashlib.new('sha256', bytes(contra, 'utf-8'))
        h = h.hexdigest()
        query = "SELECT id FROM usuario WHERE correo = %s AND contrasenia = %s"
        cursor.execute(query, (correo, h))
        id = cursor.fetchone()
        if id: #Si existe coincidencia
            return id[0], True
        else: 
            return None, False

    @classmethod
    def get_albumes(self, id):
        query = "SELECT id, titulo, anio, imagen, artistaId FROM album WHERE usuarioId = %s"
        cursor.execute(query, (id,))
        albums = []
        for row in cursor.fetchall():
            nombre_artista = Artistas.get_artista_nombre(row[4])
            album = {
                'id': row[0],
                'titulo': row[1],
                'anio': row[2],
                'imagen': row[3],
                'artistaNombre': nombre_artista
            }
            albums.append(album)
        return albums


class Artistas:
    @classmethod
    def get_artista_id(self, nombre):
        query = "SELECT id FROM artista WHERE nombre = %s"
        cursor.execute(query, (nombre,))
        id = cursor.fetchone()
        if id: #Si existe coincidencia
            return id[0]
        else: 
            return None
    
    @classmethod
    def get_artista_nombre(self, id):
        query = "SELECT nombre FROM artista WHERE id = %s"
        cursor.execute(query, (id,))
        nombre = cursor.fetchone()
        if nombre: #Si existe coincidencia
            return nombre[0]
        else: 
            return None

    @classmethod
    def existe_artista(self, nombre):
        query = "SELECT COUNT(*) FROM artista WHERE nombre = %s"
        cursor.execute(query, (nombre,))

        if cursor.fetchone()[0] == 1:
            return True
        else:
            return False

    @classmethod
    def insertar_artista(self, nombre):
        insertar = "INSERT INTO artista(nombre) VALUES (%s)"
        cursor.execute(insertar, (nombre,))
        db.commit()

        if cursor.rowcount:
            return True
        else:
            return False

class Albums:
    @classmethod
    def existe_album(self, titulo, artista):
        query = "SELECT COUNT(*) FROM album WHERE titulo = %s AND artistaId = (SELECT id FROM artista WHERE nombre = %s)"
        cursor.execute(query, (titulo, artista))

        if cursor.fetchone()[0] == 1:
            return True
        else:
            return False

    #Si no existe el artista, no existe el album
    @classmethod
    def insertar_album(self, album):
        titulo = album['titulo']
        anio = album['anio']
        imagen = album['imagen']
        usuarioId = album['usuarioId']
        nombre_artista = album['artista']

        #Validar si existe album
        if self.existe_album(titulo, nombre_artista):
            return False
        else:
            if Artistas.existe_artista(nombre_artista):
                artista_id = Artistas.get_artista_id(nombre_artista)
                insert_query = "INSERT INTO album (titulo, anio, imagen, usuarioId, artistaId) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(insert_query, (titulo, anio, imagen, usuarioId, artista_id))
                db.commit()

                if cursor.rowcount:
                    return True
                else:
                    return False
            else:
                if Artistas.insertar_artista(nombre_artista):
                    artista_id = Artistas.get_artista_id(nombre_artista)
                    insert_query = "INSERT INTO album (titulo, anio, imagen, usuarioId, artistaId) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(insert_query, (titulo, anio, imagen, usuarioId, artista_id))
                    db.commit()

                    if cursor.rowcount:
                        return True
                    else:
                        return False
                else: #No se pudo insertar el artista, no se puede crear el album
                    return False

    @classmethod
    def get_albumes(self):
        query = "SELECT id, titulo, anio, imagen, artistaId FROM album"
        cursor.execute(query)
        albums = []
        for row in cursor.fetchall():
            nombre_artista = Artistas.get_artista_nombre(row[4])
            album = {
                'id': row[0],
                'titulo': row[1],
                'anio': row[2],
                'imagen': row[3],
                'artistaNombre': nombre_artista
            }
            albums.append(album)
        return albums





