"""VAD + Whisper-small (sherpa-onnx) transcription. Usage: transcribe.py OUT_DIR clip.mp4..."""
import json, subprocess, sys
from pathlib import Path
import numpy as np
import sherpa_onnx

M = Path(__file__).parent / "models"
W = M / "sherpa-onnx-whisper-small"
SR = 16000

rec = sherpa_onnx.OfflineRecognizer.from_whisper(
    encoder=str(W / "small-encoder.int8.onnx"),
    decoder=str(W / "small-decoder.int8.onnx"),
    tokens=str(W / "small-tokens.txt"),
    language="", task="transcribe", num_threads=4,
)

def load(path):
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(pcm, dtype=np.float32)

out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
lines = []
for clip in sys.argv[2:]:
    audio = load(clip)
    cfg = sherpa_onnx.VadModelConfig()
    cfg.silero_vad.model = str(M / "silero_vad.onnx")
    cfg.silero_vad.threshold = 0.5
    cfg.silero_vad.min_silence_duration = 0.4
    cfg.silero_vad.min_speech_duration = 0.3
    cfg.silero_vad.max_speech_duration = 20
    cfg.sample_rate = SR
    vad = sherpa_onnx.VoiceActivityDetector(cfg, buffer_size_in_seconds=120)
    segs = []
    win = cfg.silero_vad.window_size
    for i in range(0, len(audio), win):
        vad.accept_waveform(audio[i:i + win])
        while not vad.empty():
            segs.append((vad.front.start, np.array(vad.front.samples))); vad.pop()
    vad.flush()
    while not vad.empty():
        segs.append((vad.front.start, np.array(vad.front.samples))); vad.pop()
    res = []
    for start, samples in segs:
        s = rec.create_stream(); s.accept_waveform(SR, samples); rec.decode_stream(s)
        r = s.result
        res.append({"start": round(start / SR, 2), "end": round((start + len(samples)) / SR, 2),
                    "text": r.text.strip(), "lang": getattr(r, "lang", "")})
    name = Path(clip).stem
    (out / f"{name}.json").write_text(json.dumps({"clip": name, "duration": round(len(audio) / SR, 2), "segments": res}, ensure_ascii=False, indent=1))
    lines.append(f"## {name}  (duration: {len(audio)/SR:.1f}s, {len(res)} speech segments)")
    lines += [f"  [{r['start']:06.2f}-{r['end']:06.2f}] {r['lang']} {r['text']}" for r in res]
    print(lines[-len(res) - 1] if res else lines[-1], flush=True)
(out / "takes_packed.md").write_text("\n".join(lines) + "\n")
