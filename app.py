from flask import Flask, jsonify, request
from youtube_transcript_api import YouTubeTranscriptApi
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "YouTube Transcript API",
        "status": "running",
        "endpoints": {
            "GET /": "This help message",
            "GET /transcript/<video_id>": "Get transcript for a YouTube video",
            "GET /transcript/<video_id>?lang=pt": "Get transcript in specific language"
        },
        "example": "/transcript/dQw4w9WgXcQ"
    })

@app.route('/transcript/<video_id>')
def get_transcript(video_id):
    try:
        # Pegar parâmetros da query
        languages = request.args.get('lang', 'en').split(',')
        
        # Inicializar a API
        api = YouTubeTranscriptApi()
        
        # Buscar transcript
        transcript = api.fetch(video_id, languages=languages)
        
        # Converter para formato JSON serializável
        transcript_data = []
        for snippet in transcript:
            transcript_data.append({
                'text': snippet.text,
                'start': snippet.start,
                'duration': snippet.duration
            })
        
        return jsonify({
            "video_id": video_id,
            "language": transcript.language,
            "language_code": transcript.language_code,
            "is_generated": transcript.is_generated,
            "transcript": transcript_data
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "video_id": video_id
        }), 400

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
