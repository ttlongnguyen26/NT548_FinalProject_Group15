from flask import Flask, request, jsonify, send_file, send_from_directory
import re
from gtts import gTTS  # Replace with Piper if needed
import os

app = Flask(__name__)

# Dictionary for common abbreviation replacements
ABBREVIATIONS = {
    "km": "kilometer",
    "w": "watt",
    "min": "minute",
    "sec": "second",
    "hr": "hour",
    # Add more abbreviations as needed
}

# Function to preprocess text
def preprocess_text(text):
    # Replace newlines and special characters with commas
    text = re.sub(r"[\n\?~]", ",", text)

    # Replace abbreviations with full forms
    for abbr, full in ABBREVIATIONS.items():
        text = re.sub(rf"\b{abbr}\b", full, text, flags=re.IGNORECASE)
    
    return text

# Endpoint to serve index.html
@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")

# Endpoint to convert text to speech
@app.route("/convert", methods=["POST"])
def convert_text_to_audio():
    try:
        # Parse JSON input from request
        data = request.json
        if not data:
            return jsonify({"error": "Invalid input. Please provide text and language."}), 400
        
        text = data.get("text", "").strip()
        lang = data.get("lang", "en").strip()

        # Validate input
        if not text:
            return jsonify({"error": "Text is required."}), 400
        if not lang:
            return jsonify({"error": "Language is required."}), 400

        # Preprocess text
        processed_text = preprocess_text(text)
        
        # Convert text to audio using gTTS (or Piper)
        tts = gTTS(text=processed_text, lang=lang)
        output_file = "output.mp3"
        tts.save(output_file)

        # Return the audio file to the frontend
        return send_file(output_file, mimetype="audio/mpeg", as_attachment=False)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Ensure the static folder is where the index.html is stored
    os.makedirs("static", exist_ok=True)
    # Ensure your index.html file is in the "static" directory
    app.run(debug=True, host="0.0.0.0", port=5000)
