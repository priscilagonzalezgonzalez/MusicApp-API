import mysql.connector
import hashlib

#database connection
db = mysql.connector.connect(
    user='sarahi', password='12345678',
    database='musicapp')

#cursor
cursor = db.cursor()


def existe_columna(nombre_tabla, nombre_columna):
    query = "SELECT count(*) " \
            "FROM INFORMATION_SCHEMA.COLUMNS " \
            "WHERE TABLE_SCHEMA = Database() AND TABLE_NAME = %s AND COLUMN_NAME = %s;"
    cursor.execute(query, (nombre_tabla, nombre_columna))
    if cursor.fetchone()[0] == 1:
        return True
    return False

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
    def get_id_usuario(self, correo, contra):
        if self.existe_usuario(correo):
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
    def crear_usuario(self, nombre, apellido, correo, contra):
        if self.existe_usuario(correo):
            return False
        else:
            h = hashlib.new('sha256', bytes(contra, 'utf-8'))
            h = h.hexdigest()
            insert_query = "INSERT INTO usuario(correo, contrasenia, nombre, apellido) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (correo, h, nombre, apellido))
            db.commit()
            if cursor.rowcount > 0:
                return self.get_id_usuario(correo, contra)
            else:
                return None, False

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
    def modificar_usuario(self, usuarioId, columna, valor):
        update = f"UPDATE usuario SET {columna} = %s WHERE id = %s"
        cursor.execute(update, (valor, usuarioId))
        db.commit()

        if cursor.rowcount:
            return True
        else:
            return False

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
        if Artistas.existe_artista(nombre):
            return False
            
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

    @classmethod
    def modificar_artista(self, id, columna, valor):
        if not existe_columna("artista", columna):
            return False

        query = f"UPDATE artista SET {columna}=%s WHERE id=%s"
        cursor.execute(query, (valor,id))
        db.commit()
        if cursor.rowcount > 0:
            return True
        return False

    @classmethod
    def get_artistas(self):
        query = "SELECT id, biografia, nombre, imagen FROM artista"
        cursor.execute(query)
        artistas = []
        for row in cursor.fetchall():
            artista = {
                'id': row[0],
                'biografia': row[1],
                'nombre': row[2],
                'imagen': row[3]
            }
            artistas.append(artista)
        return artistas

class Albums:
    @classmethod
    def existe_album(self, titulo, artista):
        query = "SELECT COUNT(*) FROM album WHERE titulo = %s AND artistaId = (SELECT id FROM artista WHERE nombre = %s)"
        cursor.execute(query, (titulo, artista))

        if cursor.fetchone()[0] == 1:
            return True
        else:
            return False

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
    def modificar_album(self, album_id, columna, valor):
        update = f"UPDATE album SET {columna} = %s WHERE id = %s"
        cursor.execute(update, (valor, album_id))
        db.commit()

        if cursor.rowcount:
            return True
        else:
            return False

    @classmethod
    def eliminar_album(self, album_id):
        delete = "DELETE from album WHERE id = %s"
        cursor.execute(delete, (album_id,))
        db.commit()

        if cursor.rowcount:
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

    @classmethod
    def get_albumes_artista(self, artistaId):
        query = "SELECT id, titulo, anio, imagen FROM album WHERE artistaId = %s"
        cursor.execute(query, (artistaId,))
        albums = []
        for row in cursor.fetchall():
            album = {
                'id': row[0],
                'titulo': row[1],
                'anio': row[2],
                'imagen': row[3]
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
    def get_tracks_album(self, id):
        query = "SELECT id, titulo, archivo, albumId FROM track WHERE albumId = %s"
        cursor.execute(query, (id,))
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
    
    @classmethod
    def modificar_track(self, track_id, columna, valor):
        update = f"UPDATE track SET {columna} = %s WHERE id = %s"
        cursor.execute(update, (valor, track_id))
        db.commit()

        if cursor.rowcount:
            return True
        else:
            return False

    @classmethod
    def eliminar_track(self, track_id):
        delete = "DELETE from track WHERE id = %s"
        cursor.execute(delete, (track_id,))
        db.commit()

        if cursor.rowcount:
            return True
        else:
            return False

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
        
class Track_Fav:
    @classmethod
    def get_fav_usuario(self, usuarioId:int):
        query = "SELECT track.id, titulo, archivo, albumId FROM track " \
                "INNER JOIN fav_track ON track.id = fav_track.trackId " \
                "WHERE fav_track.usuarioId = %s "

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
    def es_fav(self, usuarioId, trackId):
        query = "SELECT COUNT(*) FROM fav_track WHERE usuarioId = %s and trackId = %s"
        cursor.execute(query, (usuarioId, trackId))
        print("HEEEELLOOOO \n")
        
        if cursor.fetchone()[0] > 0:
            return True
        else:
            return False

    @classmethod
    def agregar_fav(self, usuarioId, trackId):
        if self.es_fav(usuarioId, trackId):
            return False
        else:
            insert_query = "INSERT INTO fav_track(usuarioId, trackId) VALUES (%s, %s)"
            cursor.execute(insert_query, (usuarioId, trackId))
            db.commit()
            if cursor.rowcount > 0:
                return True
            else:
                return False
    
    @classmethod
    def eliminar_fav(self, usuarioId, trackId):
        if not self.es_fav(usuarioId, trackId):
            return False
        else:
            delete = "DELETE from fav_track WHERE usuarioId = %s and trackId = %s"
            cursor.execute(delete, (usuarioId, trackId))
            db.commit()

            if cursor.rowcount:
                return True
            else:
                return False

class Album_Fav:
    @classmethod
    def get_fav_usuario(self, usuarioId:int):
        query = "SELECT album.id, titulo, anio, imagen, artistaId FROM album " \
                "INNER JOIN fav_album ON album.id = fav_album.albumId " \
                "WHERE fav_album.usuarioId = %s "

        cursor.execute(query, (usuarioId,))
        return [
            {
                'id':row[0],
                'titulo':row[1],
                'anio':row[2],
                'imagen':row[3],
                'artistaNombre': Artistas.get_artista_nombre(row[4])
            }
            for row in cursor.fetchall()
        ]

    @classmethod
    def es_fav(self, usuarioId, albumId):
        query = "SELECT COUNT(*) FROM fav_album WHERE usuarioId = %s and albumId = %s"
        cursor.execute(query, (usuarioId, albumId))

        if cursor.fetchone() > 0:
            return True
        else:
            return False

    @classmethod
    def agregar_fav(self, usuarioId, albumId):
        if self.es_fav(usuarioId, albumId):
            return False
        else:
            insert_query = "INSERT INTO fav_album(usuarioId, albumId) VALUES (%s, %s)"
            cursor.execute(insert_query, (usuarioId, albumId))
            db.commit()
            if cursor.rowcount > 0:
                return True
            else:
                return False
    
    @classmethod
    def eliminar_fav(self, usuarioId, albumId):
        if not self.es_fav(usuarioId, albumId):
            return False
        else:
            delete = "DELETE from fav_album WHERE usuarioId = %s and albumId = %s"
            cursor.execute(delete, (usuarioId, albumId))
            db.commit()

            if cursor.rowcount:
                return True
            else:
                return False