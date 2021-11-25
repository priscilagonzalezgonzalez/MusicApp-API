from flask import Flask, json, request, jsonify

from conexion import Track_Fav, Tracks, Usuarios, Artistas, Albums, Album_Fav

#crea una aplicación con el nombre del archivo
app = Flask(__name__)

#Rutas de Usuario
@app.route("/api/v1/usuarios", methods=["POST"]) 
@app.route("/api/v1/usuarios/<int:id>", methods=["PATCH"]) 
@app.route("/api/v1/usuarios/<int:id>/albumes", methods=["GET"]) 
@app.route("/api/v1/usuarios/<int:id>/albumes/<int:album_id>", methods=["GET", "PATCH", "DELETE"]) 
def usuario(id = None, album_id = None):
    if request.method == "POST" and request.is_json:
        try: 
            data = request.get_json()
            id, ok = Usuarios.crear_usuario(data['nombre'], data['apellido'], data['correo'], data['contraseña'])
            if ok:
                return jsonify({"code": "ok", "id": id})
            else:
                return jsonify({"code": "noexiste"})
        except:
            return jsonify({"code": "error"}) 

    elif request.method == "PATCH" and id is not None and album_id is None and request.is_json:
        try:
            data = request.get_json()
            columna = data['columna']
            valor = data['valor']

            if Usuarios.modificar_usuario(id, columna, valor):
                return jsonify({"code": "ok"})
            else:
                return jsonify({"code": "no"})
        except:
            return jsonify({"code":"error"})

    elif request.method == "GET" and id is not None and album_id is None:
        return jsonify(Usuarios.get_albumes(id))

    elif request.method == "GET" and id is not None and album_id is not None:
        return jsonify(Tracks.get_tracks_album(album_id))
    
    elif request.method == "PATCH" and id is not None and album_id is not None and request.is_json:
        try:
            data = request.get_json()
            columna = data['columna']
            valor = data['valor']

            if Albums.modificar_album(id, album_id, columna, valor):
                return jsonify({"code": "ok"})
            else:
                return jsonify({"code": "no"})
        except:
            return jsonify({"code": "error"})

    elif request.method == "DELETE" and id is not None and album_id is not None:
        if Albums.eliminar_album(album_id):
            return jsonify({"code": "ok"})
        else:
            return jsonify({"code": "no"})

# Rutas para las caciones favoritas del usuario
@app.route("/api/v1/usuario/<int:usuarioId>/tracks_fav", methods=["POST", "GET"])
@app.route("/api/v1/usuario/<int:usuarioId>/tracks_fav/<int:trackId>", methods=["POST", "DELETE"])
def canciones_favoritas(usuarioId=None, trackId=None):
    # Obtiene todas las canciones favoritas del usuario
    if request.method == "GET" and usuarioId is not None:
        try:
            return jsonify(Track_Fav.get_fav_usuario(usuarioId))
        except:
            return jsonify({"code": "error"})
    # Agrega una canción favorita por medio de un json
    elif request.method == "POST" and usuarioId is not None and request.is_json:
        try:
            data = request.get_json()
            trackId = data["trackId"]
            if Track_Fav.agregar_fav(usuarioId, trackId):
                return jsonify({"code": "ok"})
            else:
                return jsonify({"code": "no"})
        except:
            return jsonify({"code": "error"})
    # Agrega una canción favorita por solo la URL
    elif request.method == "POST" and usuarioId is not None and trackId is not None:
        try:
            if Track_Fav.agregar_fav(usuarioId, trackId):
                return jsonify({"code": "ok"})
            else:
                return jsonify({"code": "no"})
        except:
            return jsonify({"code": "error"})
    # Elimina una cancion favorita
    elif request.method == "DELETE" and usuarioId is not None and trackId is not None:
        try:
            if Track_Fav.eliminar_fav(usuarioId, trackId):
                return jsonify({"code": "ok"})
            else:
                return jsonify({"code": "no"})
        except:
            return jsonify({"code": "error"})
    # Si no se puede procesar la solicitud, devuelve:
    return jsonify({"code": "none"})

# Rutas para los albumes favoritos del usuario
@app.route("/api/v1/usuario/<int:usuarioId>/albumes_fav", methods=["POST", "GET"])
@app.route("/api/v1/usuario/<int:usuarioId>/albumes_fav/<int:albumId>", methods=["POST", "DELETE"])
def albumes_favoritos(usuarioId=None, albumId=None):
    # Obtiene todos los albumes favoritos del usuario
    if request.method == "GET" and usuarioId is not None:
        try:
            return jsonify(Album_Fav.get_fav_usuario(usuarioId))
        except:
            return jsonify({"code": "error"})
    # Agrega un album a favorito por medio de un json
    elif request.method == "POST" and usuarioId is not None and request.is_json:
        try:
            data = request.get_json()
            albumId = data["albumId"]
            if Album_Fav.agregar_fav(usuarioId, albumId):
                return jsonify({"code": "ok"})
            else:
                return jsonify({"code": "no"})
        except:
            return jsonify({"code": "error"})
    # Agrega un album favorito por solo la URL
    elif request.method == "POST" and usuarioId is not None and albumId is not None:
        try:
            if Album_Fav.agregar_fav(usuarioId, albumId):
                return jsonify({"code": "ok"})
            else:
                return jsonify({"code": "no"})
        except:
            return jsonify({"code": "error"})
    # Elimina una album favorito
    elif request.method == "DELETE" and usuarioId is not None and albumId is not None:
        try:
            if Album_Fav.eliminar_fav(usuarioId, albumId):
                return jsonify({"code": "ok"})
            else:
                return jsonify({"code": "no"})
        except:
            return jsonify({"code": "error"})
    # Si no se puede procesar la solicitud, devuelve:
    return jsonify({"code": "none"})

#Rutas de Albumes
@app.route("/api/v1/albumes", methods=["GET", "POST"])
@app.route("/api/v1/albumes/<int:id>", methods=["GET"])
def albumes(id = None):
    if request.method == "POST" and request.is_json:
        try:
            data = request.get_json()
            if Albums.insertar_album(data):
                return jsonify({"code": "ok"})
            else:
                return jsonify({"code": "no"})
        except:
            return jsonify({"code": "error"})
            
    elif request.method == "GET" and id is None:
        return jsonify(Albums.get_albumes())

    elif request.method == "GET" and id is not None:
        return jsonify(Albums.get_album(id))

#Ruta para tracks de album
@app.route("/api/v1/albumes/<int:id>/tracks", methods=["GET"])
def albumes_tracks(id = None):
    if request.method == "GET":
        return jsonify(Tracks.get_tracks_album(id))

#Ruta albumes de un artista
@app.route("/api/v1/artistas/<int:artistaId>/albums", methods=["GET"])
def albumes_artista(artistaId):
    if request.method == "GET" and artistaId is not None:
        return jsonify(Albums.get_albumes_artista(artistaId))

#Rutas de Sesiones
@app.route("/api/v1/sesiones", methods=["POST"]) #Inicio de sesión
def sesion():
    if request.method == "POST" and request.is_json:
        try:
            data = request.get_json()
            correo = data['correo']
            contra = data['contraseña']
            id, ok = Usuarios.iniciar_sesion(correo, contra)
            if ok:
                return jsonify({"code": "ok", "id": id})
            else:
                return jsonify({"code": "noexiste"})
        except:
            return jsonify({"code": "error"}) 

#Rutas de Artistas
@app.route("/api/v1/artistas", methods=["GET", "POST"])
@app.route("/api/v1/artistas/<int:id>", methods=["GET", "PATCH"])
def artistas(id=None):
    if request.method == "POST" and request.is_json:
        try:
            data = request.get_json()
            nombre = data['nombre']
            if Artistas.insertar_artista(nombre):
                return jsonify({"code":"ok"})
            else:
                return jsonify({"code":"no"})
        except:
            return jsonify({"code":"error"})
            
    elif request.method == "GET" and id is None:
        try:
            return jsonify(Artistas.get_artistas())
        except:
            return jsonify({"code":"error"})

    elif request.method == "GET" and id is not None:
        artista = Artistas.get_artista(id)
        if artista:
            return jsonify(artista)
        else:
            return jsonify({"code":f"artist with id = {id} does not exist"})

    elif request.method == "PATCH" and id is not None and request.is_json:
        data = request.get_json()
        columna = data['columna']
        valor = data['valor']

        if Artistas.modificar_artista(id, columna, valor):
            return jsonify({"code": "ok"})
        else:
            return jsonify({"code": "no"})

    return jsonify({"code":"None"})


#Rutas para Tracks
@app.route("/api/v1/tracks", methods=["POST", "GET"])
@app.route("/api/v1/tracks/<int:id>", methods=["PATCH", "GET", "DELETE"])
def tracks(id = None):
    if request.method == "POST" and request.is_json:
        try:
            data = request.get_json()
            if Tracks.insertar_track(data):
                return jsonify({"code":"ok"})
            else:
                return jsonify({"code":"no"})
        except:
            return jsonify({"code":"error"})
    
    elif request.method == "GET":
        return jsonify(Tracks.get_tracks())

    elif request.method == "GET" and id is not None:
        return jsonify(Tracks.get_track(id))
    
    elif request.method == "PATCH" and id is not None:
        try:
            data = request.get_json()
            columna = data["columna"]
            valor = data["valor"]
            if Tracks.modificar_track(id, columna, valor):
                return jsonify({"code":"ok"})
            else:
                return jsonify({"code":"no"})
        except:
            return jsonify({"code":"error"})

    elif request.method == "DELETE" and id is not None:
        try:
            if Tracks.eliminar_track(id):
                return jsonify({"code":"ok"})
            else:
                return jsonify({"code":"no"})
        except:
            return jsonify({"code":"error"})

app.run(debug=True)