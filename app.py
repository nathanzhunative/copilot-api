from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Mock sessions database
sessions = [
    {
        "sessionName": "Q3 Planning with Alex",
        "date": "2025-07-15",
        "attendees": ["Alex", "Jordan", "Nathan"],
        "summary": "Reviewed roadmap and hiring priorities.",
        "transcript": "Long transcript text...",
        "snapshots": ["url1", "url2"]
    },
    {
        "sessionName": "Marketing Sync",
        "date": "2025-07-18",
        "attendees": ["Sam", "Jordan"],
        "summary": "Reviewed campaign results.",
        "transcript": "Another transcript...",
        "snapshots": ["url3"]
    }
]
@app.route("/sessions", methods=["GET"])
def get_everything():
    return jsonify(sessions)

# @app.route("/sessions", methods=["GET"])
# def get_sessions():
#     attendee = request.args.get("attendee")
#     if attendee:
#         filtered = [s for s in sessions if attendee in s["attendees"]]
#         return jsonify(filtered)
#     return jsonify(sessions)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)