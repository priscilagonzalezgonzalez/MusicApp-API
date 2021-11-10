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

        if cursor.rowcount > 0:
            return True
        else:
            return False

    @classmethod
    def get_artista(self, id:int):
        query = "SELECT biografia, nombre, imagen FROM artista WHERE id = %s"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        if cursor.rowcount > 0:
            return {
                'biografia':row[0],
                'nombre':row[1],
                'imagen':row[2]
            }
        else:
            return None

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
        elif not Artistas.existe_artista(nombre_artista):
            if not Artistas.insertar_artista(nombre_artista):
                return False

        artista_id = Artistas.get_artista_id(nombre_artista)
        insert_query = "INSERT INTO album (titulo, anio, imagen, usuarioId, artistaId) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (titulo, anio, imagen, usuarioId, artista_id))
        db.commit()

        if cursor.rowcount > 0:
            return True
        else:
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

    @classmethod
    def get_album(self, id:int):
        query = "SELECT titulo, anio, imagen, artistaId FROM album WHERE id = %s"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        if cursor.rowcount > 0:
            return {
                'titulo': row[0],
                'anio': row[1],
                'imagen': row[2],
                'artistaNombre': Artistas.get_artista_nombre(row[3])
            }
        else:
            return None

    @classmethod
    def get_albumes_usuario(self, id):
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

class Tracks:
    @classmethod
    def existe_track(self, titulo:str, albumId:int):
        query = "SELECT COUNT(*) FROM track WHERE titulo = %s AND albumId = %s"
        cursor.execute(query, (titulo, albumId))

        if cursor.fetchone()[0] == 1:
            return True
        return False

    @classmethod
    def insertar_track(self, track):
        titulo = track['titulo']
        archivo = track['archivo']
        albumId = track['albumId']

        if self.existe_track(titulo, albumId):
            return False
        
        query = "INSERT INTO track (titulo, archivo, albumId) VALUES (%s, %s, %s)"
        cursor.execute(query, (titulo, archivo, albumId))
        db.commit()

        if cursor.rowcount > 0:
            return True
        else:
            return False
    
    @classmethod
    def get_tracks(self):
        query = "SELECT id, titulo, archivo, albumId FROM track"
        cursor.execute(query)
        return [
            {
                'id':row[0],
                'titulo':row[1],
                'archivo':row[2],
                'albumId':row[3]
            }
            for row in cursor.fetchall()
        ]

    @classmethod
    def get_tracks_usuario(self, usuarioId:int):
        query = "SELECT id, titulo, archivo, albumId FROM track WHERE albumId IN (SELECT id FROM album WHERE usuarioId = %s)"
        cursor.execute(query, (usuarioId,))
        return [
            {
                'id':row[0],
                'titulo':row[1],
                'archivo':row[2],
                'albumId':row[3]
            }
            for row in cursor.fetchall()
        ]

    @classmethod
    def get_track(self, id:int):
        query = "SELECT titulo, archivo, albumId FROM track WHERE id = %s"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        if cursor.rowcount > 0:
            return {
                'titulo':row[0],
                'archivo':row[1],
                'albumId':row[2]
            }
        else:
            return None

class Resenia:
    @classmethod
    def existe_resenia(self, usuarioId:int, albumId:int):
        query = "SELECT COUNT(*) FROM resenia WHERE usuarioId = %s AND albumId = %s"
        cursor.execute(query, (usuarioId, albumId))

        if cursor.fetchone()[0] == 1:
            return True
        return False

    @classmethod
    def insertar_resenia(self, resenia):
        texto = resenia['texto']
        usuarioId = resenia['usuarioId']
        albumId = resenia['albumId']

        if self.existe_resenia(usuarioId, albumId):
            return False

        query = "INSERT INTO resenia (texto, fecha, usuarioId, albumId) VALUES (%s, now(), %s, %s)"
        cursor.execute(query, (texto, usuarioId, albumId))
        db.commit()

        if cursor.rowcount > 0:
            return True
        return False

    @classmethod
    def get_resenias_usuario(self, usuarioId:int):
        query = "SELECT id, texto, fecha, albumId FROM resenia WHERE usuarioId = %s"
        cursor.execute(query, (usuarioId,))
        return [
            {
                'id' : row[0], 
                'texto' : row[1], 
                'fecha' : row[2], 
                'albumId' : row[3]
            }
            for row in cursor.fetchall()
        ]

    @classmethod
    def get_resenias_album(self, albumId:int):
        query = "SELECT id, texto, fecha, usuarioId FROM resenia WHERE albumId = %s"
        cursor.execute(query, (albumId,))
        return [
            {
                'id' : row[0], 
                'texto' : row[1], 
                'fecha' : row[2], 
                'usuarioId' : row[3]
            }
            for row in cursor.fetchall()
        ]

    @classmethod
    def eliminar_resenia(self, usuarioId:int, albumId:int):
        if not self.existe_resenia(usuarioId, albumId):
            return False

        query = "DELETE FROM resenia WHERE usuarioId = %s AND albumId = %s"
        cursor.execute(query, (usuarioId, albumId))
        db.commit()

        if cursor.rowcount > 0:
            return True
        return False
        