from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import os
import tempfile
import uuid

app = Flask(__name__)
CORS(app)

@app.route('/extract-audio', methods=['POST'])
def extract_audio():
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
            
        if 'tiktok.com' not in url:
            return jsonify({'error': 'Invalid TikTok URL'}), 400
        
        # Create temporary file
        temp_dir = tempfile.gettempdir()
        filename = f"tiktok_audio_{uuid.uuid4().hex}.mp3"
        output_path = os.path.join(temp_dir, filename)
        
        # yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path,
            'extractaudio': True,
            'audioformat': 'mp3',
            'audioquality': '0',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        if os.path.exists(output_path):
            return send_file(output_path, as_attachment=True, download_name=filename)
        else:
            return jsonify({'error': 'Audio extraction failed'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
