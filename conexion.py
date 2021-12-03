import mysql.connector
import hashlib

#database connection
def connector():
    """ return mysql.connector.connect(
        host='sql3.freesqldatabase.com',
        user='sql3455954', 
        password='reuRhF8JtJ',
        database='sql3455954'
    ) """
    return mysql.connector.connect(
        user='sarahi', password='12345678',
        database='musicapp'
    )

def existe_columna(nombre_tabla, nombre_columna):
    try:
        db = connector()
        cursor = db.cursor()
    
        query = "SELECT count(*) " \
                "FROM INFORMATION_SCHEMA.COLUMNS " \
                "WHERE TABLE_SCHEMA = Database() AND TABLE_NAME = %s AND COLUMN_NAME = %s;"
        cursor.execute(query, (nombre_tabla, nombre_columna))
        if cursor.fetchone()[0] == 1:
            return True
        return False
    finally:
        if db:
            cursor.close()
            db.close()

class Usuarios:
    @classmethod
    def existe_usuario(self, correo):
        try:
            db = connector()
            cursor = db.cursor()
        
            query = "SELECT COUNT(*) FROM usuario WHERE correo = %s"
            cursor.execute(query, (correo,))

            if cursor.fetchone()[0] == 1:
                return True
            else:
                return False
        finally:
            if db:
                cursor.close()
                db.close()
                
    @classmethod
    def get_id_usuario(self, correo, contra):
        try:
            db = connector()
            cursor = db.cursor()
        
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
        finally:
            if db:
                cursor.close()
                db.close()


    @classmethod
    def crear_usuario(self, nombre, apellido, correo, contra):
        try:
            db = connector()
            cursor = db.cursor()
        
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
        finally:
            if db:
                cursor.close()
                db.close()

    @classmethod
    def iniciar_sesion(self, correo, contra):
        try:
            db = connector()
            cursor = db.cursor()
        
            h = hashlib.new('sha256', bytes(contra, 'utf-8'))
            h = h.hexdigest()
            query = "SELECT id FROM usuario WHERE correo = %s AND contrasenia = %s"
            cursor.execute(query, (correo, h))
            id = cursor.fetchone()
            if id: #Si existe coincidencia
                return id[0], True
            else: 
                return None, False
        finally:
            if db:
                cursor.close()
                db.close()

    @classmethod
    def modificar_usuario(self, usuarioId, columna, valor):
        try:
            db = connector()
            cursor = db.cursor()
        
            update = f"UPDATE usuario SET {columna} = %s WHERE id = %s"
            cursor.execute(update, (valor, usuarioId))
            db.commit()

            if cursor.rowcount:
                return True
            else:
                return False
        finally:
            if db:
                cursor.close()
                db.close()

class Artistas:
    @classmethod
    def get_artista_id(self, nombre):
        try:
            db = connector()
            cursor = db.cursor()
        
            query = "SELECT id FROM artista WHERE nombre = %s"
            cursor.execute(query, (nombre,))
            id = cursor.fetchone()
            if id: #Si existe coincidencia
                return id[0]
            else: 
                return None
        finally:
            if db:
                cursor.close()
                db.close()
    
    @classmethod
    def get_artista_nombre(self, id):
        try:
            db = connector()
            cursor = db.cursor()
        
            query = "SELECT nombre FROM artista WHERE id = %s"
            cursor.execute(query, (id,))
            nombre = cursor.fetchone()
            if nombre: #Si existe coincidencia
                return nombre[0]
            else: 
                return None
        finally:
            if db:
                cursor.close()
                db.close()

    @classmethod
    def existe_artista(self, nombre):
        try:
            db = connector()
            cursor = db.cursor()
        
            query = "SELECT COUNT(*) FROM artista WHERE nombre = %s"
            cursor.execute(query, (nombre,))

            if cursor.fetchone()[0] == 1:
                return True
            else:
                return False
        finally:
            if db:
                cursor.close()
                db.close()

    @classmethod
    def insertar_artista_with_name(self, nombre, usuarioId):
        try:
            db = connector()
            cursor = db.cursor()
        
            if Artistas.existe_artista(nombre):
                return False
                
            insertar = "INSERT INTO artista(nombre, usuarioId) VALUES (%s, %s)"
            cursor.execute(insertar, (nombre, usuarioId))
            db.commit()

            if cursor.rowcount > 0:
                return True
            else:
                return False
        finally:
            if db:
                cursor.close()
                db.close()

    @classmethod
    def insertar_artista(self, artista):
        try:
            db = connector()
            cursor = db.cursor()

            nombre = artista['nombre']
            biografia = artista['biografia']
            imagen = artista['imagen']
            usuarioId = artista['usuarioId']
        
            if Artistas.existe_artista(nombre):
                return False
                
            insertar = "INSERT INTO artista(nombre, biografia, imagen, usuarioId) VALUES (%s, %s, %s, %s)"
            cursor.execute(insertar, (nombre, biografia, imagen, usuarioId))
            db.commit()

            if cursor.rowcount > 0:
                return True
            else:
                return False
        finally:
            if db:
                cursor.close()
                db.close()

    @classmethod
    def get_artista(self, id:int):
        try:
            db = connector()
            cursor = db.cursor()
        
            query = "SELECT biografia, nombre, imagen, usuarioId, id " \
                    "FROM artista WHERE id = %s "

            cursor.execute(query, (id,))
            row = cursor.fetchone()
            if cursor.rowcount > 0:
                return {
                    'biografia':row[0],
                    'nombre':row[1],
                    'imagen':row[2],
                    'usuarioId':row[3],
                    'id':row[4]
                }
            else:
                return None
        except mysql.connector.Error as e:
            print(f"Error at <get_artista>\n    query = {query}\n{str(e)}")
            return False
        finally:
            if db:
                cursor.close()
                db.close()

    @classmethod
    def modificar_artista(self, id, columna, valor):
        try:
            db = connector()
            cursor = db.cursor()
        
            if not existe_columna("artista", columna):
                return False

            query = f"UPDATE artista SET {columna}=%s WHERE id=%s"
            cursor.execute(query, (valor,id))
            db.commit()
            if cursor.rowcount > 0:
                return True
            return False
        finally:
            if db:
                cursor.close()
                db.close()

    @classmethod
    def get_artistas(self):
        try:
            db = connector()
            cursor = db.cursor()
        
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
        finally:
            if db:
                cursor.close()
                db.close()
    
    @classmethod
    def get_artistas_usuario(self, usuarioId):
        try:
            db = connector()
            cursor = db.cursor()

            query = "SELECT id, biografia, nombre, imagen " \
                    "FROM artista WHERE usuarioId = %s "

            cursor.execute(query, (usuarioId,))
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
        except mysql.connector.Error as e:
            print(f"Error at <get_artistas_usuarios>\n    query = {query}\n{str(e)}")
            return False
        finally:
            if db:
                cursor.close()
                db.close()

class Albums:
    @classmethod
    def existe_album(self, titulo, artista):
        try:
            db = connector()
            cursor = db.cursor()
        
            query = "SELECT COUNT(*) FROM album WHERE titulo = %s AND artistaId = (SELECT id FROM artista WHERE nombre = %s)"
            cursor.execute(query, (titulo, artista))

            if cursor.fetchone()[0] == 1:
                return True
            else:
                return False
        finally:
            if db:
                cursor.close()
                db.close()

    @classmethod
    def insertar_album(self, album):
        try:
            db = connector()
            cursor = db.cursor()
        
            titulo = album['titulo']
            anio = album['anio']
            imagen = album['imagen']
            usuarioId = album['usuarioId']
            nombre_artista = album['artista']

            #Validar si existe album
            if self.existe_album(titulo, nombre_artista):
                return False
            elif not Artistas.existe_artista(nombre_artista):
                if not Artistas.insertar_artista_with_name(nombre_artista, usuarioId):
                    return False

            artista_id = Artistas.get_artista_id(nombre_artista)
            insert_query = "INSERT INTO album (titulo, anio, imagen, usuarioId, artistaId) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (titulo, anio, imagen, usuarioId, artista_id))
            db.commit()

            if cursor.rowcount > 0:
                return True
            else:
                return False
        finally:
            if db:
                cursor.close()
                db.close()

    @classmethod
    def modificar_album(self, usuarioId, album_id, columna, valor):
        try:
            db = connector()
            cursor = db.cursor()
        
            if not existe_columna("album", columna):
                return False

            update = f"UPDATE album SET {columna} = %s WHERE id = %s and usuarioId = %s"
            cursor.execute(update, (valor, album_id, usuarioId))
            db.commit()

            if cursor.rowcount:
                return True
            else:
                return False
        finally:
            if db:
                cursor.close()
                db.close()

    @classmethod
    def eliminar_album(self, usuarioId, album_id):
        try:
            db = connector()
            cursor = db.cursor()
        
            delete = "DELETE from album WHERE id = %s and usuarioId = %s"
            cursor.execute(delete, (album_id, usuarioId))
            db.commit()

            if cursor.rowcount:
                return True
            else:
                return False
        finally:
            if db:
                cursor.close()
                db.close()

    @classmethod
    def get_albumes(self):
        try:
            db = connector()
            cursor = db.cursor()
        
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
        finally:
            if db:
                cursor.close()
                db.close()

    @classmethod
    def get_album(self, id):
        try:
            db = connector()
            cursor = db.cursor()
        
            query = "SELECT album.titulo, album.anio, album.imagen, album.usuarioId, artista.nombre FROM album " \
                    "INNER JOIN artista ON album.artistaId = artista.id " \
                    "WHERE album.id = %s "
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            if cursor.rowcount > 0:
                return {
                    'titulo': row[0],
                    'anio': row[1],
                    'imagen': row[2],
                    'usuarioId': row[3],
                    'artistaNombre': row[4]
                }
            else:
                return None
        finally:
            if db:
                cursor.close()
                db.close()

    @classmethod
    def get_albumes_usuario(self, id):
        try:
            db = connector()
            cursor = db.cursor()
        
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
        finally:
            if db:
                cursor.close()
                db.close()

    @classmethod
    def get_albumes_artista(self, artistaId):
        try:
            db = connector()
            cursor = db.cursor()
        
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
        finally:
            if db:
                cursor.close()
                db.close()

class Tracks:
    @classmethod
    def existe_track(self, titulo:str, albumId:int):
        try:
            db = connector()
            cursor = db.cursor()
        
            query = "SELECT COUNT(*) FROM track WHERE titulo = %s AND albumId = %s"
            cursor.execute(query, (titulo, albumId))

            if cursor.fetchone()[0] == 1:
                return True
            return False
        finally:
            if db:
                cursor.close()
                db.close()

    @classmethod
    def insertar_track(self, track):
        try:
            db = connector()
            cursor = db.cursor()
        
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
        finally:
            if db:
                cursor.close()
                db.close()
    
    @classmethod
    def get_tracks(self):
        try:
            db = connector()
            cursor = db.cursor()
        
            query = "SELECT track.id, track.titulo, track.archivo, album.id, album.titulo, artista.nombre " \
                    "FROM track " \
                    "INNER JOIN album " \
                        "ON track.albumId = album.id " \
                    "INNER JOIN artista " \
                        "ON album.artistaId = artista.id " \

            cursor.execute(query)
            return [
                {
                    'id':row[0],
                    'titulo':row[1],
                    'archivo':row[2],
                    'albumId':row[3],
                    'albumTitulo':row[4],
                    'artista':row[5]
                }
                for row in cursor.fetchall()
            ]
        finally:
            if db:
                cursor.close()
                db.close()

    @classmethod
    def get_tracks_album(self, id):
        try:
            db = connector()
            cursor = db.cursor()
        
            query = "SELECT id, titulo, archivo from track WHERE albumId = %s"
            cursor.execute(query, (id,))
            tracks = []
            for row in cursor.fetchall():
                track = {
                    'id':row[0],
                    'titulo':row[1],
                    'archivo':row[2]
                }
                tracks.append(track)
            return tracks
        finally:
            if db:
                cursor.close()
                db.close()

    @classmethod
    def get_tracks_usuario(self, usuarioId:int):
        try:
            db = connector()
            cursor = db.cursor()
        
            query = "SELECT track.id, track.titulo, archivo, albumId, album.titulo, album.imagen FROM track " \
                    "INNER JOIN album ON track.albumId = album.id "\
                    "WHERE album.usuarioId = %s "
            cursor.execute(query, (usuarioId,))
            return [
                {
                    'id':row[0],
                    'titulo':row[1],
                    'archivo':row[2],
                    'albumId':row[3],
                    'albumTitulo':row[4],
                    'imagen':row[5]
                }
                for row in cursor.fetchall()
            ]
        finally:
            if db:
                cursor.close()
                db.close()

    @classmethod
    def get_track(self, id:int):
        try:
            db = connector()
            cursor = db.cursor()
        
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
        finally:
            if db:
                cursor.close()
                db.close()
    
    @classmethod
    def modificar_track(self, track_id, columna, valor):
        try:
            db = connector()
            cursor = db.cursor()
        
            update = f"UPDATE track SET {columna} = %s WHERE id = %s"
            cursor.execute(update, (valor, track_id))
            db.commit()

            if cursor.rowcount:
                return True
            else:
                return False
        finally:
            if db:
                cursor.close()
                db.close()

    @classmethod
    def eliminar_track(self, track_id):
        try:
            db = connector()
            cursor = db.cursor()
        
            delete = "DELETE from track WHERE id = %s"
            cursor.execute(delete, (track_id,))
            db.commit()

            if cursor.rowcount:
                return True
            else:
                return False
        finally:
            if db:
                cursor.close()
                db.close()

class Resenia:
    @classmethod
    def existe_resenia(self, usuarioId:int, albumId:int):
        try:
            db = connector()
            cursor = db.cursor()
        
            query = "SELECT COUNT(*) FROM resenia WHERE usuarioId = %s AND albumId = %s"
            cursor.execute(query, (usuarioId, albumId))

            if cursor.fetchone()[0] == 1:
                return True
            return False
        finally:
            if db:
                cursor.close()
                db.close()

    @classmethod
    def insertar_resenia(self, resenia):
        try:
            db = connector()
            cursor = db.cursor()
        
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
        finally:
            if db:
                cursor.close()
                db.close()

    @classmethod
    def get_resenias_usuario(self, usuarioId:int):
        try:
            db = connector()
            cursor = db.cursor()
        
            query = "SELECT resenia.id, resenia.texto, resenia.fecha, album.id, album.titulo, artista.nombre, album.imagen FROM resenia " \
                    "INNER JOIN album ON resenia.albumId = album.id " \
                    "INNER JOIN artista ON album.artistaId = artista.id " \
                    "WHERE resenia.usuarioId = %s " 

            cursor.execute(query, (usuarioId,))
            return [
                {
                    'id' : row[0], 
                    'texto' : row[1], 
                    'fecha' : row[2], 
                    'album' : {
                        'id' : row[3],
                        'titulo' : row[4],
                        'artistaNombre' : row[5],
                        'imagen':row[6]
                    }
                }
                for row in cursor.fetchall()
            ]
        finally:
            if db:
                cursor.close()
                db.close()

    @classmethod
    def get_resenias_album(self, albumId:int):
        try:
            db = connector()
            cursor = db.cursor()
        
            query = "SELECT resenia.id, resenia.texto, resenia.fecha, usuario.nombre, usuario.apellido " \
                    "FROM resenia " \
                    "INNER JOIN usuario ON resenia.usuarioId = usuario.id " \
                    "WHERE resenia.albumId = %s "

            cursor.execute(query, (albumId,))
            return [
                {
                    'id' : row[0], 
                    'texto' : row[1], 
                    'fecha' : row[2], 
                    'usuario' : f"{row[3]} {row[4]}"
                }
                for row in cursor.fetchall()
            ]
        finally:
            if db:
                cursor.close()
                db.close()

    @classmethod
    def eliminar_resenia(self, usuarioId:int, albumId:int):
        try:
            db = connector()
            cursor = db.cursor()
        
            if not self.existe_resenia(usuarioId, albumId):
                return False

            query = "DELETE FROM resenia WHERE usuarioId = %s AND albumId = %s"
            cursor.execute(query, (usuarioId, albumId))
            db.commit()

            if cursor.rowcount > 0:
                return True
            return False
        finally:
            if db:
                cursor.close()
                db.close()
        
class Track_Fav:
    @classmethod
    def get_fav_usuario(self, usuarioId:int):
        try:
            db = connector()
            cursor = db.cursor()
        
            query = "SELECT track.id, track.titulo, archivo, albumId, album.titulo, album.imagen FROM track " \
                    "INNER JOIN fav_track ON track.id = fav_track.trackId " \
                    "INNER JOIN album ON track.albumId = album.id "\
                    "WHERE fav_track.usuarioId = %s "

            cursor.execute(query, (usuarioId,))
            return [
                {
                    'id':row[0],
                    'titulo':row[1],
                    'archivo':row[2],
                    'albumId':row[3],
                    'albumTitulo':row[4],
                    'imagen':row[5]
                }
                for row in cursor.fetchall()
            ]
        finally:
            if db:
                cursor.close()
                db.close()
    
    @classmethod
    def es_fav(self, usuarioId, trackId):
        try:
            db = connector()
            cursor = db.cursor()
        
            query = "SELECT COUNT(*) FROM fav_track WHERE usuarioId = %s and trackId = %s"
            cursor.execute(query, (usuarioId, trackId))
            
            if cursor.fetchone()[0] > 0:
                return True
            else:
                return False
        finally:
            if db:
                cursor.close()
                db.close()

    @classmethod
    def agregar_fav(self, usuarioId, trackId):
        try:
            db = connector()
            cursor = db.cursor()
        
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
        finally:
            if db:
                cursor.close()
                db.close()
    
    @classmethod
    def eliminar_fav(self, usuarioId, trackId):
        try:
            db = connector()
            cursor = db.cursor()
        
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
        finally:
            if db:
                cursor.close()
                db.close()

class Album_Fav:
    @classmethod
    def get_fav_usuario(self, usuarioId:int):
        try:
            db = connector()
            cursor = db.cursor()
        
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
        finally:
            if db:
                cursor.close()
                db.close()

    @classmethod
    def es_fav(self, usuarioId, albumId):
        try:
            db = connector()
            cursor = db.cursor()
        
            query = "SELECT COUNT(*) FROM fav_album WHERE usuarioId = %s and albumId = %s"
            cursor.execute(query, (usuarioId, albumId))

            if cursor.fetchone()[0] > 0:
                return True
            else:
                return False
        finally:
            if db:
                cursor.close()
                db.close()

    @classmethod
    def agregar_fav(self, usuarioId, albumId):
        try:
            db = connector()
            cursor = db.cursor()
        
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
        finally:
            if db:
                cursor.close()
                db.close()
    
    @classmethod
    def eliminar_fav(self, usuarioId, albumId):
        try:
            db = connector()
            cursor = db.cursor()
        
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
        finally:
            if db:
                cursor.close()
                db.close()