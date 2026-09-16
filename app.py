from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp
from faster_whisper import WhisperModel
import os
import tempfile

app = Flask(__name__)
model = WhisperModel("tiny", device="cpu", compute_type="int8")

@app.route('/transcript', methods=['GET'])
def get_transcript():
    video_id = request.args.get('video_id')
    video_url = request.args.get('video_url')
    lang = request.args.get('lang', 'en')

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang, 'en'])
        text = " ".join([t['text'] for t in transcript])
        return jsonify({"success": True, "source": "captions", "transcript": text})
    except Exception:
        pass

    try:
        temp_dir = tempfile.gettempdir()
        audio_path = os.path.join(temp_dir, f"{video_id}.mp3")
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(temp_dir, f"{video_id}.%(ext)s"),
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        segments, _ = model.transcribe(audio_path)
        text = " ".join([seg.text for seg in segments])
        os.remove(audio_path)

        return jsonify({"success": True, "source": "whisper", "transcript": text})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/', methods=['GET'])
def health():
    return jsonify({"status": "running"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))