# YouTube Video Assistant

A multilingual AI assistant that answers questions about any YouTube video, grounded in its actual transcript.

## What it does
Paste a YouTube link, ask a question (or ask for a summary), and get an answer generated from the video's real transcript — not a hallucinated guess. Supports English, Hindi, and Malayalam.

## How it works
1. **Transcript extraction** (Flask + yt-dlp): pulls YouTube captions when available
2. **Whisper fallback** (faster-whisper): transcribes audio directly when no captions exist
3. **Orchestration** (n8n): routes the transcript + user question to an LLM
4. **Answer generation** (Google Gemini): produces a grounded, transcript-based response
5. **Frontend** (HTML/Tailwind/JS): simple interface to submit a video + question
## n8n Workflow
The orchestration logic — webhook → transcript service → Gemini → JSON response — is available as an importable n8n workflow: [`n8n-workflow.json`](./n8n-workflow.json)

> Note: the transcript service URL in this export points to a local ngrok tunnel used during development. Replace it with your own hosted endpoint when importing.

## Tech stack
Flask · yt-dlp · faster-whisper · n8n · Google Gemini API · HTML/Tailwind/JS

## Setup
1. Clone this repo
2. `pip install -r requirements.txt`
3. Run `python app.py`
4. Expose it publicly (e.g. via ngrok) if connecting to a hosted n8n workflow
5. Open `index.html` in a browser

## Notes
- Captions-first approach; Whisper fallback works but is limited by YouTube's bot-detection on cloud IPs, so it's most reliable run locally/residentially.