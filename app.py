from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

# 讀取 .env 檔
load_dotenv()

app = Flask(__name__)
CORS(app)

# 從環境變數取得資料庫連線字串
DATABASE_URL = os.getenv("DATABASE_URL")
connection = psycopg2.connect(DATABASE_URL)

ALLOWED_TABLES = {
    "article", "mail", "inventory", "experience", "member", "bank", "cloud",
    "routine", "host", "subscription", "video", "food"
}

def select_table(table_name):
    if table_name not in ALLOWED_TABLES:
        raise ValueError("Invalid table name")
    with connection.cursor() as cursor:
        query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name))
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]

@app.route("/")
def index():
    return "Hello, Flask with dynamic table query!"

@app.route('/api/<string:table_name>')
def get_table_data(table_name):
    try:
        result = select_table(table_name)
        return jsonify(result)
    except ValueError:
        return jsonify({"error": "Invalid table name"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tables')
def list_tables():
    return jsonify(sorted(list(ALLOWED_TABLES)))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
