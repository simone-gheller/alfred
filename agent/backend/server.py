from flask import Flask, request, jsonify
import os
from load_pipeline import load_pipeline

app = Flask(__name__)

PIPELINE_STORAGE = "pipelines"

@app.route("/upload", methods=["POST"])
def upload_pipeline():
    file = request.files["file"]
    file_path = os.path.join(PIPELINE_STORAGE, file.filename)
    file.save(file_path)
    return jsonify({"message": "Pipeline saved!", "path": file_path})

@app.route("/run", methods=["POST"])
def run_pipeline():
    data = request.json
    pipeline_file = os.path.join(PIPELINE_STORAGE, data["filename"])
    
    if not os.path.exists(pipeline_file):
        return jsonify({"error": "Pipeline not found"}), 404

    pipeline = load_pipeline(pipeline_file)
    result = 'boh'
    
    return jsonify({"output": result})

if __name__ == "__main__":
    os.makedirs(PIPELINE_STORAGE, exist_ok=True)
    app.run(port=5000, debug=True)
