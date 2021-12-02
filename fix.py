from conexion import *

if __name__ == "__main__":
    db = connector()
    cursor = db.cursor()
    
    if not existe_columna("artista", "usuarioId"):
        query = "alter table artista add usuarioId INT UNSIGNED NOT NULL"
        cursor.execute(query)
        db.commit()

    query = "SELECT id FROM usuario LIMIT 1 "
    cursor.execute(query)
    usuario_bendito = cursor.fetchone()[0]

    query = "SELECT artista.id, album.usuarioId " \
            "FROM artista " \
            "LEFT JOIN album ON album.artistaId = artista.id "
    cursor.execute(query)

    for row in cursor.fetchall():
        id_artista = row[0]
        id_usuario = row[1]

        if id_usuario is None:
            id_usuario = usuario_bendito
        Artistas.modificar_artista(id_artista, "usuarioId", id_usuario)
    
