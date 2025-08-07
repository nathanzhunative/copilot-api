from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)

SESSIONS_DIR = "../sessions"

def load_sessions():
    sessions = []
    if not os.path.exists(SESSIONS_DIR):
        return sessions
    for session_folder in os.listdir(SESSIONS_DIR):
        print(f"Loading session from folder: {session_folder}")
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

def get_everything():
    sessions = load_sessions()
    return jsonify(sessions)

def home():
    return "API is live", 200

def test():
    print("Test function called")
    print(load_sessions())
    print(get_everything())

test()