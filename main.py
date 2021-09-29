from flask import Flask, request, jsonify

from conexion import crear_usuario, iniciar_sesion
from conexion import insertar_album

#crea una aplicación con el nombre del archivo
app = Flask(__name__)


@app.route("/api/v1/usuarios", methods=["POST"]) #Registrar
def usuario():
    if request.method == "POST" and request.is_json:
            data = request.get_json()
            print(data)

            if crear_usuario(data['nombre'], data['apellido'], data['correo'], data['contraseña']):
                return jsonify({"code": "ok"})
            else:
                return jsonify({"code": "existe"})

@app.route("/api/v1/albumes", methods=["GET", "POST"])
def albumes():
    if request.method == "POST" and request.is_json:
        data = request.get_json()
        print(data)
        if insertar_album(data):
            return jsonify({"code": "ok"})
        else:
            return jsonify({"code": "no"})


@app.route("/api/v1/sesiones", methods=["POST"]) #Inicio de sesión
def sesion():
    if request.method == "POST" and request.is_json:
        try:
            data = request.get_json()
            correo = data['correo']
            contra = data['contraseña']
            id, ok = iniciar_sesion(correo, contra)
            if ok:
                return jsonify({"code": "ok", "id": id})
            else:
                return jsonify({"code": "noexiste"})
        except:
            return jsonify({"code": "error"})



app.run(debug=True)