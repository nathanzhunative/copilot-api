from flask import Flask
from routes import meetings_bp, assets_bp
import os

app = Flask(__name__)
app.register_blueprint(meetings_bp)
app.register_blueprint(assets_bp)

# Render deployment
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host="0.0.0.0", port=port)

# local deployment
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)