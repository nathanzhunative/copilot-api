from flask import Flask, request, jsonify
import os
import json

# app = Flask(__name__)

SESSIONS_DIR = "sessions"

def load_sessions() -> list[dict]:
    '''
    Load session data from the sessions directory.
    '''
    print('loading sessions')
    sessions = []
    if not os.path.exists(SESSIONS_DIR):
        print('no sessions found')
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
    print('lookie here', sessions[1])
    print('lookie here', len(sessions))
    return sessions

load_sessions()
print('played')
# def get_everything():
#     sessions = load_sessions()
#     return jsonify(sessions)

# def home():
#     return "API is live", 200

# def test():
#     print("Test function called")
#     print(load_sessions())
#     # print(get_everything())

# test()