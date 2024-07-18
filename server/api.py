from flask import Blueprint, request, jsonify
from scraper import scrape_forex_data
from database import get_db

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/forex-data', methods=['GET','POST'])
def forex_data():
    from_currency = request.args.get('from')
    to_currency = request.args.get('to')
    period1 = request.args.get('period1')
    period2 = request.args.get('period2')

    if not all([from_currency, to_currency, period1, period2]):
        return jsonify({"error": "Missing required parameters"}), 400
    try:
        df = scrape_forex_data(from_currency, to_currency, period1, period2)
        df.to_sql(f"{from_currency}_{to_currency}_{period1}_{period2}", get_db(), if_exists='replace', index=False)
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500