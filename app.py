from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
import re

app = Flask(__name__)
CORS(app)

url = 'postgresql://postgres:JXedgMYPPpAYrQyegtxYZvwQEmAXNLBi@trolley.proxy.rlwy.net:39115/railway'
connection = psycopg2.connect(url)

# ✅ 合法的資料表名稱清單
ALLOWED_TABLES = {
    "article", "mail", "inventory", "experience", "member", "bank", "cloud",
    "routine", "host", "subscription", "video", "food"
}

def select_table(table_name):
    # ✅ 安全性檢查
    if table_name not in ALLOWED_TABLES:
        raise ValueError("Invalid table name")

    with connection.cursor() as cursor:
        query = f"SELECT * FROM {table_name};"
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        result = [dict(zip(columns, row)) for row in rows]
    return result

@app.route("/")
def index():
    return "Hello, Flask with dynamic table query!"

# ✅ 動態路由：例如 /api/bank, /api/article...
@app.route('/api/<table_name>')
def get_table_data(table_name):
    try:
        result = select_table(table_name)
        return jsonify(result)
    except ValueError:
        return jsonify({"error": "Invalid table name"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
