from flask import Flask
from flask_cors import CORS
from api import api_bp
from database import init_db

app = Flask(__name__)
CORS(app)
app.register_blueprint(api_bp)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)