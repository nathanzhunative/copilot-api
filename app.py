# from flask import Flask, request, jsonify
# import os

# app = Flask(__name__)

# # Mock sessions database
# sessions = [
#     {
#         "sessionName": "Q3 Planning with Alex",
#         "date": "2025-07-15",
#         "attendees": ["Alex", "Jordan", "Nathan"],
#         "summary": "Reviewed roadmap and hiring priorities.",
#         "transcript": "Long transcript text...",
#         "snapshots": ["url1", "url2"]
#     },
#     {
#         "sessionName": "Marketing Sync",
#         "date": "2025-07-18",
#         "attendees": ["Sam", "Jordan"],
#         "summary": "Reviewed campaign results.",
#         "transcript": "Another transcript...",
#         "snapshots": ["url3"]
#     }
# ]
# @app.route("/sessions", methods=["GET"])
# def get_everything():
#     return jsonify(sessions)

# @app.route("/", methods=["GET"])
# def home():
#     return "API is live", 200

# # @app.route("/sessions", methods=["GET"])
# # def get_sessions():
# #     attendee = request.args.get("attendee")
# #     if attendee:
# #         filtered = [s for s in sessions if attendee in s["attendees"]]
# #         return jsonify(filtered)
# #     return jsonify(sessions)

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host="0.0.0.0", port=port)
from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)

SESSIONS_DIR = "sessions"

def load_sessions():
    sessions = []
    if not os.path.exists(SESSIONS_DIR):
        return sessions
    for session_folder in os.listdir(SESSIONS_DIR):
        folder_path = os.path.join(SESSIONS_DIR, session_folder)
        if os.path.isdir(folder_path):
            metadata_path = os.path.join(folder_path, "metadata.txt")
            transcript_path = os.path.join(folder_path, "transcript.txt")
            if os.path.exists(metadata_path):
                try:
                    with open(metadata_path, "r") as meta_file:
                        # Try to parse as JSON, fallback to key-value pairs
                        try:
                            metadata = json.load(meta_file)
                        except json.JSONDecodeError:
                            meta_file.seek(0)
                            metadata = {}
                            for line in meta_file:
                                if ":" in line:
                                    key, value = line.split(":", 1)
                                    metadata[key.strip()] = value.strip()
                    transcript = ""
                    if os.path.exists(transcript_path):
                        with open(transcript_path, "r") as t_file:
                            transcript = t_file.read()
                    metadata["transcript"] = transcript
                    sessions.append(metadata)
                except Exception as e:
                    print(f"Error loading session in {folder_path}: {e}")
    return sessions

@app.route("/sessions", methods=["GET"])
def get_everything():
    sessions = load_sessions()
    return jsonify(sessions)

@app.route("/", methods=["GET"])
def home():
    return "API is live", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)