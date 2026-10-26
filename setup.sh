#!/usr/bin/env bash
# Re-install the vertical-video (9:16, 1080x1920) editing toolchain for Claude Code.
# Follows the official guides: video-use/install.md and the HyperFrames README.
# Safe to re-run. Remotion is intentionally NOT installed (install only on request).
set -euo pipefail

echo "== Base tools =="
for c in node npm python3 git ffmpeg ffprobe claude; do
  command -v "$c" >/dev/null || { echo "MISSING: $c — install it first"; exit 1; }
done
node -e 'process.exit(+process.versions.node.split(".")[0] >= 22 ? 0 : 1)' \
  || { echo "Node.js 22+ required (HyperFrames)"; exit 1; }
command -v uv >/dev/null || pip install uv

echo "== yt-dlp =="
command -v yt-dlp >/dev/null || uv tool install yt-dlp

echo "== video-use =="
VU="$HOME/Developer/video-use"
if [ -d "$VU" ]; then git -C "$VU" pull --ff-only; else git clone https://github.com/browser-use/video-use "$VU"; fi
(cd "$VU" && uv sync)
mkdir -p "$HOME/.claude/skills"
ln -sfn "$VU" "$HOME/.claude/skills/video-use"

echo "== HyperFrames =="
claude plugin marketplace add heygen-com/hyperframes || true
claude plugin install hyperframes@hyperframes || true
npx --yes hyperframes skills update
npx --yes hyperframes browser ensure

echo "== ElevenLabs key =="
if [ -n "${ELEVENLABS_API_KEY:-}" ] || grep -q '^ELEVENLABS_API_KEY=..' "$VU/.env" 2>/dev/null; then
  echo "ElevenLabs key found"
else
  echo "No ElevenLabs key yet — add ELEVENLABS_API_KEY to $VU/.env (chmod 600)"
fi

echo "Done."
