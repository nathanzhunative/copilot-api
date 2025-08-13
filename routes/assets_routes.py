from flask import Blueprint, send_file
from qdrant_client.http import models as qm
from config import client
from flask import jsonify

# Define a new Blueprint named "assets"
bp = Blueprint("assets", __name__)

@bp.get("/assets/health")
def health():
    return jsonify({"status": "ok"})

@bp.get("/assets/<meeting_id>/<asset_type>")
def get_asset(meeting_id, asset_type):
    # We need to find the specific asset in the "assets" collection
    # that matches the meeting_id and the asset_type.

    # Construct the filter for the Qdrant query
    # This filter searches for points where the meetingId matches the one from the URL
    # and the type matches the requested asset type (e.g., 'snapshot', 'audio')
    asset_filter = qm.Filter(
        must=[
            qm.FieldCondition(
                key="meetingId",
                match=qm.MatchValue(value=meeting_id)
            ),
            qm.FieldCondition(
                key="type",
                match=qm.MatchValue(value=asset_type)
            )
        ]
    )

    # Perform the search in the "assets" collection
    search_result = client.scroll(
        collection_name="assets",
        scroll_filter=asset_filter,
        limit=1,  # We only need one result
        with_payload=True,
        with_vectors=False
    )

    # Check if a point was found
    if not search_result[0]:
        return {"error": "Asset not found"}, 404

    # Get the payload and the path to the asset from the search result
    asset_payload = search_result[0][0].payload
    asset_path = asset_payload.get("path")

    if not asset_path:
        return {"error": "Asset path not found in payload"}, 404

    # Assuming your files are stored in a local directory on the server
    # You would need to change this path to point to your actual file storage location
    file_path = f"/path/to/your/asset/storage/{asset_path}"

    try:
        # Determine the MIME type based on the asset type
        mimetype = "image/png" if asset_type == "snapshot" else "audio/wav" # Add other types as needed
        return send_file(file_path, mimetype=mimetype)
    except FileNotFoundError:
        return {"error": "File not found on disk"}, 404