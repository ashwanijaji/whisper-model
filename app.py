import whisper
import os
import uuid
from flask import Flask, request, jsonify, send_from_directory, send_file


app = Flask(__name__)
model = whisper.load_model("base")  # Replace 'base' with your model name


@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({'text': '', 'success': False, 'error': 'No file uploaded'})

    # Generate unique filename to avoid conflicts
    file = request.files['file']
    filename = f"{uuid.uuid4()}.{file.filename.split('.')[-1]}"  # Extract extension
    
    # Validate allowed extensions (modify as needed)
    allowed_extensions = ['wav', 'flac', 'ogg', 'mp3' ]
    if filename.split('.')[-1].lower() not in allowed_extensions:
        return jsonify({'error': 'Unsupported file format. Allowed formats: ' + ', '.join(allowed_extensions)})

    # Temporary file path (modify 'uploads' as desired)
    file_path = os.path.join("uploads", filename)

    try:
        # Save the uploaded file
        file.save(file_path)

        # Load audio using the saved path
        audio = whisper.load_audio(file_path)

        result = model.transcribe(audio)
        # Delete the temporary file after transcription
        os.remove(file_path)

        return jsonify({'text': result['text'], 'success': True}) 
    except Exception as e:
        # Handle potential errors during saving or transcription
        print(f"Error during transcription: {e}")
        return jsonify({'text': '', 'success': False, 'error': 'An error occurred during transcription.'})
    # ... after transcription code ...
@app.route('/download_text', methods=['POST'])
def download_text():
    data = request.get_json()
    text = data['text']

    filename = "transcript.txt"
    with open(filename, 'w') as f:
        f.write(text)

    return send_file(filename, as_attachment=True)

    
@app.route('/')
def index():
    return send_from_directory('static', 'index.html') 

if __name__ == '__main__':
    app.run(debug=True)
