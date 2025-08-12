from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime, timedelta
from qdrant_client import QdrantClient

app = Flask(__name__)

api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.NcmjVSfeHQ3cAY4APa83Shyp5ZSHpJxTKFghiNwleJA"

client = QdrantClient(
    url="https://f9c6c053-eeee-4a80-87b2-f7e32152180c.us-east4-0.gcp.cloud.qdrant.io",
    api_key=api_key
)