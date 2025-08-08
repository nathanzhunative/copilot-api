from flask import Flask, request, jsonify, send_from_directory
import os
import json
from datetime import datetime, timedelta

app = Flask(__name__)

SESSIONS_DIR = "sessions"

def load_sessions() -> list[dict]:
    '''
    Load session data from the sessions directory.
    '''
    sessions = []
    if not os.path.exists(SESSIONS_DIR):
        return sessions
    
    BASE_URL = "https://copilot-api-1.onrender.com"

    # Iterate through each session folder
    for session_folder in os.listdir(SESSIONS_DIR):
        folder_path = os.path.join(SESSIONS_DIR, session_folder)
        if os.path.isdir(folder_path):
            metadata_path = os.path.join(folder_path, "metadata.txt")
            transcript_path = os.path.join(folder_path, "transcript.txt")
            images = []

            for fname in os.listdir(folder_path):
                if fname.endswith(".png") or fname.endswith(".jpg") or fname.startswith("image"):
                    url_path = f"/sessions/{session_folder}/{fname}"
                    images.append(f"{BASE_URL}{url_path}")

            if os.path.exists(metadata_path):
                try:
                    with open(metadata_path, "r") as meta_file:
                        # Try to parse metadata file as JSON
                        try:
                            metadata = json.load(meta_file)
                        except json.JSONDecodeError:
                            meta_file.seek(0)
                            metadata = {}
                            for line in meta_file:
                                if ":" in line:
                                    key, value = line.split(":", 1)
                                    metadata[key.strip()] = value.strip()
                                    
                    # Load transcript into the metadata
                    transcript = ""
                    if os.path.exists(transcript_path):
                        with open(transcript_path, "r") as t_file:
                            transcript = t_file.read()

                    metadata["transcript"] = transcript
                    metadata["images"] = images
                    sessions.append(metadata)
                except Exception as e:
                    print(f"Error loading session in {folder_path}: {e}")
    return sessions

@app.route("/sessions", methods=["GET"])
def get_everything():
    sessions = load_sessions()
    return jsonify(sessions)

@app.route("/sessions/recent", methods=["GET"])
def get_recent_sessions():
    try:
        days = int(request.args.get("days", 7))
    except ValueError:
        return jsonify({"error": "Invalid 'days' parameter"}), 400
    now = datetime.utcnow()
    cutoff = now - timedelta(days=days)
    sessions = load_sessions()

    recent = [
        s for s in sessions
        if "startTime" in s and datetime.fromisoformat(s["startTime"].replace("Z", "+00:00")) >= cutoff
    ]
    return jsonify(recent)

@app.route("/sessions/actions", methods=["GET"])
def get_all_actions():
    sessions = load_sessions()
    all_actions = []

    for s in sessions:
        for action in s.get("actions", []):
            # Optionally include session context
            all_actions.append({
                "session": s.get("name"),
                **action
            })
    return jsonify(all_actions)

@app.route("/sessions/summary", methods=["GET"])
def get_session_summaries():
    sessions = load_sessions()
    summaries = [
        {
            "name": s.get("name"),
            "date": s.get("startTime"),
            "summary": s.get("summary")
        }
        for s in sessions
    ]
    return jsonify(summaries)


@app.route("/", methods=["GET"])
def home():
    return "API is live", 200

@app.route("/sessions/by_attendee", methods=["GET"])
def get_sessions_by_attendee():
    attendee = request.args.get("name")
    if not attendee:
        return jsonify({"error": "Missing 'name' parameter"}), 400
    sessions = load_sessions()
    filtered = [s for s in sessions if attendee in s.get("attendees", [])]
    return jsonify(filtered)

@app.route("/sessions/by_date", methods=["GET"])
def get_sessions_by_date():
    start = request.args.get("from")
    end = request.args.get("to")
    try:
        start_dt = datetime.fromisoformat(start) if start else datetime.min
        end_dt = datetime.fromisoformat(end) if end else datetime.max
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD or ISO 8601."}), 400

    sessions = load_sessions()
    filtered = [
        s for s in sessions
        if "startTime" in s and start_dt <= datetime.fromisoformat(s["startTime"].replace("Z", "+00:00")) <= end_dt
    ]
    return jsonify(filtered)

@app.route("/sessions/topics", methods=["GET"])
def get_all_topics():
    sessions = load_sessions()
    # Use keywords from summaries to simulate "topics"
    topics = set()
    for s in sessions:
        summary = s.get("summary", "")
        for word in summary.split():
            if word.istitle() and len(word) > 3:  # crude filter for capitalized words
                topics.add(word.strip(".,"))
    return jsonify(sorted(topics))

@app.route("/sessions/<session_id>/<image_name>")
def get_image(session_id, image_name):
    image_path = os.path.join(SESSIONS_DIR, session_id)
    return send_from_directory(image_path, image_name)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)