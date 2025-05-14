import src.database as database

from flask_cors import CORS
from flask import Flask, jsonify


app = Flask(__name__)
CORS(app)


@app.route("/api/data/<item_name>", methods=['GET'])
def get_data( item_name ):
    
    r = database.query_database(
        """
            SELECT Item.item_name, Data.json, Data.created_at 
            FROM Data
            LEFT JOIN Item ON Data.item_id = Item.id
            WHERE Item.item_name = ?
        """,
        ( item_name, )
    )

    return jsonify(r)


@app.route("/api/items", methods=['GET'])
def get_all_items():
    
    r = database.query_database(
        """
        SELECT item_name, item_url FROM Item
        ORDER BY item_name
        """
    )
        
    return jsonify(r)


if __name__ == '__main__':
    database.initialize_db()
    app.run(debug=True)