# REVIEW — "POV: 3 intern, 1 event" (9:16, 1080x1920, 40.5 s)

## Creative calls
- Ikut storyboard pengguna (9 babak) tetapi disesuaikan dengan footage POV MIHAS: Food Hunter (aiskrim ube, sambal, brownies), The Intellectual (booth JAKIM/Halal, sesi soal jawab, seminar, networking), The Corporate Survivor (team Bubbles bawa beg, jurugambar, selfie eskalator, jalan tanpa henti).
- Hook: frame 0 sudah ada "POV: Bila 3 intern pergi event yang sama..." atas reveal dewan pameran (MAIN STAGE).
- Setiap watak dibuka dengan colour-flood (pink/biru/kuning) yang bertukar jadi chip tajuk; sticker kertas putih + doodle kuning ikut gaya storyboard. Font: Permanent Marker + Kalam 700.
- Dibuang: v_12 (terbalik), v_18 (pinggan sisa), pergerakan kamera bergoncang, pengulangan jalan kaki.

## Measured
- `hyperframes check`: 0 error. Amaran disimpan: `timeline_track_too_dense` (sticker per babak), `container_overflow` (punch-in footage), `line_unread` finale 2.87 s vs 3.07 s (shot selfie tamat sebelum dia berpaling).
- Muka: semakan snapshot — sticker diletak di bahagian bawah/dada, tidak menutup muka (e2, e3, f2, f3, h1).
- Safe zone: teks antara y 168–1330 px, tepi kanan ≤ 940 px.
- Audio (draf): −17.2 LUFS, true peak −1.5 dBTP, tiada clipping. Diukur, tidak didengar.

## Belum
- Muzik latar: tiada sumber berlesen yang boleh dicapai dari rangkaian sesi ini. Slot `<audio id="bgm">` disediakan dalam index.html; bunyi ambien klip (0.4) perlu diturunkan ke ~0.25 bila muzik ditambah.
- Transkripsi: ElevenLabs disekat; guna Whisper-small tempatan (sherpa-onnx). Hampir tiada dialog — video dipacu muzik/visual.
