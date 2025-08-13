from flask import Blueprint, request, jsonify
from qdrant_client.http import models as qm
from config import client

bp = Blueprint("qdrant", __name__)

@bp.get("/collections")
def list_collections():
    info = client.get_collections()
    return jsonify([c.name for c in info.collections])

@bp.get("/collections/<name>/sample")
def collection_sample(name):
    pts, _ = client.scroll(name, limit=5, with_payload=True, with_vectors=False)
    return jsonify([{"id": p.id, "payload": p.payload} for p in pts])

@bp.get("/similar")
def similar():
    name = request.args.get("collection", "assets")
    pid = request.args.get("id")
    k = int(request.args.get("k", 5))
    res = client.recommend(name, positive=[pid], limit=k, with_payload=True)
    return jsonify([{"id": r.id, "score": r.score, "payload": r.payload} for r in res])