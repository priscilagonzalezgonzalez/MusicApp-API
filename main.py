from flask import Flask, json, request, jsonify

from conexion import Tracks, Usuarios, Artistas, Albums

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
            
            if Usuarios.crear_usuario(data['nombre'], data['apellido'], data['correo'], data['contraseña']):
                return jsonify({"code": "ok"})
            else:
                return jsonify({"code": "existe"})
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

            if Albums.modificar_album(album_id, columna, valor):
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


#Rutas de Albumes
@app.route("/api/v1/albumes", methods=["GET", "POST"])
@app.route("/api/v1/albumes/<int:id>")
def albumes(id = None, artistaId=None):
    if request.method == "POST" and request.is_json:
        try:
            data = request.get_json()
            print(data)
            if Albums.insertar_album(data):
                return jsonify({"code": "ok"})
            else:
                return jsonify({"code": "no"})
        except:
            return jsonify({"code": "error"})
            
    elif request.method == "GET" and id is None:
        return jsonify(Albums.get_albumes())

    elif request.method == "GET" and id is not None:
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
@app.route("/api/v1/artistas/<int:id>", methods=["PATCH"])
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