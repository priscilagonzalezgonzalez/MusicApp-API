from flask import Flask, request, jsonify

from conexion import Usuarios, Artistas, Albums

#crea una aplicación con el nombre del archivo
app = Flask(__name__)


@app.route("/api/v1/usuarios", methods=["POST"]) #Registrar
@app.route("/api/v1/usuarios/<int:id>/albumes", methods=["GET"]) 
def usuario(id = None):
    if request.method == "POST" and request.is_json:
        try: 
            data = request.get_json()

            if Usuarios.crear_usuario(data['nombre'], data['apellido'], data['correo'], data['contraseña']):
                return jsonify({"code": "ok"})
            else:
                return jsonify({"code": "existe"})
        except:
            return jsonify({"code": "error"})
    elif request.method == "GET" and id is not None:
        return jsonify(Usuarios.get_albumes(id))

@app.route("/api/v1/albumes", methods=["GET", "POST"])
def albumes():
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
    elif request.method == "GET":
        return jsonify(Albums.get_albumes())


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

@app.route("/api/v1/artistas", methods=["POST"])
def artistas():
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
    else:
        return jsonify({"code":"None"})

app.run(debug=True)