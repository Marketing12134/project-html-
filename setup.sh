#!/usr/bin/env bash
# Setup video editing untuk TikTok / Instagram Reels (9:16, 1080x1920).
# Idempotent: selamat dijalankan semula dalam session baru.
set -euo pipefail

need() { command -v "$1" >/dev/null || { echo "TIADA: $1 — sila pasang dahulu"; exit 1; }; }
for c in node npm python3 uv git ffmpeg ffprobe claude; do need "$c"; done
node -e 'process.exit(+process.versions.node.split(".")[0] >= 22 ? 0 : 1)' || { echo "Node.js 22+ diperlukan"; exit 1; }

# yt-dlp
command -v yt-dlp >/dev/null || uv tool install yt-dlp

# Video-Use (ikut install.md rasmi)
VU="$HOME/Developer/video-use"
if [ -d "$VU/.git" ]; then git -C "$VU" pull --ff-only; else git clone https://github.com/browser-use/video-use "$VU"; fi
(cd "$VU" && uv sync)
mkdir -p "$HOME/.claude/skills"
ln -sfn "$VU" "$HOME/.claude/skills/video-use"

# Hyperframes (plugin Claude Code rasmi + Chrome Headless Shell untuk render)
claude plugin marketplace list 2>/dev/null | grep -q hyperframes || claude plugin marketplace add heygen-com/hyperframes
claude plugin list 2>/dev/null | grep -q 'hyperframes@hyperframes' || claude plugin install hyperframes@hyperframes
npx --yes hyperframes browser ensure

# Kunci ElevenLabs: env var ELEVENLABS_API_KEY atau $VU/.env (jangan commit)
if [ -n "${ELEVENLABS_API_KEY:-}" ] && ! grep -q '^ELEVENLABS_API_KEY=..' "$VU/.env" 2>/dev/null; then
  printf 'ELEVENLABS_API_KEY=%s\n' "$ELEVENLABS_API_KEY" > "$VU/.env" && chmod 600 "$VU/.env"
fi
grep -q '^ELEVENLABS_API_KEY=..' "$VU/.env" 2>/dev/null && echo "ElevenLabs key: ada" || echo "ElevenLabs key: BELUM ditetapkan"

echo "Setup siap."
