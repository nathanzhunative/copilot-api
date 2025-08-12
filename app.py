from flask import Flask
from routes import qdrant_bp

app = Flask(__name__)
app.register_blueprint(qdrant_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
