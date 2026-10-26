# Vertical video editing (TikTok / Instagram Reels)

Default output: 9:16, 1080x1920, H.264 MP4.

## Toolchain
- **video-use** (`~/Developer/video-use`, skill `video-use`): transcript-driven cutting, grading, subtitles. Transcription uses ElevenLabs Scribe — key in `~/Developer/video-use/.env`.
- **HyperFrames** (Claude Code plugin `hyperframes@hyperframes`): HTML-based motion graphics, captions, overlays. Scaffold portrait projects with `npx hyperframes init <name> --resolution portrait`.
- **yt-dlp**: download reference videos.
- **FFmpeg / FFprobe**: encoding and inspection.
- **Remotion**: not installed — ask the user before installing.

Re-install everything in a fresh session with `bash setup.sh`.

## Rules
- Never commit `.env` or API keys.
- Do not transcribe (it costs ElevenLabs credits) or edit footage until the user asks.
