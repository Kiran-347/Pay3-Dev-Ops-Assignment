import os
from flask import Flask, request, jsonify
import psycopg2


def get_db_connection():
        conn = psycopg2.connect(host=os.getenv("DB_HOST"),port=os.getenv("DB_PORT",5432),database=os.getenv("DB_NAME"),user=os.getenv("DB_USER"),password=os.getenv("DB_PASSWORD"))
        return conn
def check_auth(req):
        auth = req.headers.get("Authorization")
        return auth == "pay3-assignment"

app = Flask(__name__)
@app.route('/')
def home():
	return "api running"
@app.route('/create', methods=["POST"])
def create_item():
        if not check_auth(request):
                return jsonify({"error":"Unauthorized"}), 401
        data = request.get_json()
        name = data.get("name")
        value = data.get("value")
        if not name or value is None:
                return jsonify({"error":"Invalid input"}), 400
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
                "INSERT INTO items(name,value) VALUES(%s, %s)",(name,value)
                )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "item created"}), 201
@app.route('/list', methods =["GET"])
def list_items():
        if not check_auth(request):
                return jsonify({"error":"Unauthorized"}), 401
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
                "SELECT id, name, value FROM items"
                )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        items = [{"id":r[0], "name":r[1], "value":r[2]} for r in rows]
        return jsonify(items),200

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000)
