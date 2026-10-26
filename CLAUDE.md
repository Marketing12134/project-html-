# Video editing — TikTok / Instagram Reels

- Format output lalai: 9:16, 1080x1920, H.264 + AAC, 30fps (kecuali sumber lain diminta).
- Session baru: jalankan `bash setup.sh` dahulu.
- Edit video: guna skill `video-use` (`~/Developer/video-use`, baca `SKILL.md` + `helpers/`). Output dalam `<folder_video>/edit/`.
- Animasi/overlay/kapsyen: guna plugin `hyperframes` (`/hyperframes:hyperframes`), projek dengan `--resolution portrait`.
- Remotion: belum dipasang — tanya pengguna dahulu.
- Video rujukan: `yt-dlp`.
- Transkripsi: ElevenLabs Scribe (kunci dalam `~/Developer/video-use/.env`, jangan commit). Scribe berbayar — jangan transcribe tanpa arahan.
- Jangan commit fail media (mp4/mov/wav) atau `.env`.
