from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

@app.route("/")
def home():
    return "API funcionando"

# Crear usuario
@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO usuarios (nombre, email) VALUES (%s, %s)",
                (data["nombre"], data["email"]))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Usuario creado"}

# Listar usuarios
@app.route("/users", methods=["GET"])
def get_users():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuarios")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(users)

# Eliminar usuario
@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Usuario eliminado"}


# Actualizar usuario
@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.json
    conn = get_conn()
    cur = conn.cursor()
    
    cur.execute(
        "UPDATE usuarios SET nombre = %s, email = %s WHERE id = %s",
        (data["nombre"], data["email"], id)
    )
    
    conn.commit()
    cur.close()
    conn.close()
    
    return {"message": "Usuario actualizado"}



if __name__ == "__main__":
    app.run()