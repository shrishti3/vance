from flask import Blueprint, request, jsonify
from scraper import scrape_forex_data
from database import get_db
import pandas as pd

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/forex-data', methods=['GET','POST'])
def forex_data():
    from_currency = request.args.get('from')
    to_currency = request.args.get('to')
    period1 = request.args.get('period1')
    period2 = request.args.get('period2')

    if not all([from_currency, to_currency, period1, period2]):
        return jsonify({"error": "Missing required parameters"}), 400

    table_name = f"{from_currency}_{to_currency}_{period1}_{period2}"
    conn = get_db()

    # Check if table exists
    query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
    if pd.read_sql_query(query, conn).empty:
        # Table does not exist, scrape the data
        try:
            df = scrape_forex_data(from_currency, to_currency, period1, period2)
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            return jsonify(df.to_dict(orient='records'))
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        # Table exists, fetch the data
        try:
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
            return jsonify(df.to_dict(orient='records'))
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@api_bp.route('/fetch-data', methods=['GET'])
def fetch_data():
    from_currency = request.args.get('from')
    to_currency = request.args.get('to')
    period1 = request.args.get('period1')
    period2 = request.args.get('period2')

    if not all([from_currency, to_currency, period1, period2]):
        return jsonify({"error": "Missing required parameters"}), 400

    table_name = f"{from_currency}_{to_currency}_{period1}_{period2}"
    conn = get_db()

    try:
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
