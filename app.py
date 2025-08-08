from flask import Flask, request, jsonify
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
    
    # Iterate through each session folder
    for session_folder in os.listdir(SESSIONS_DIR):
        folder_path = os.path.join(SESSIONS_DIR, session_folder)
        if os.path.isdir(folder_path):
            metadata_path = os.path.join(folder_path, "metadata.txt")
            transcript_path = os.path.join(folder_path, "transcript.txt")
            images = []

            for fname in os.listdir(folder_path):
                if fname.endswith(".png") or fname.endswith(".jpg") or fname.startswith("image"):
                    images.append(os.path.join(folder_path, fname))

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)