"""Generates the intern-pov HyperFrames project (index.html + compositions/*.html)."""
import json
from pathlib import Path

P = Path("/home/user/project-html-/intern-event/edit/intern-pov")
(P / "compositions").mkdir(exist_ok=True)

C = dict(pink="#FF8FB8", blue="#7CC8F2", yellow="#FFE14D", mint="#8EE3C0",
         ink="#141414", paper="#FFFFFF", spark="#FFD60A", green="#2BB673")

FONTS = """
    @font-face { font-family: "Permanent Marker"; src: url("assets/fonts/permanent-marker.woff2") format("woff2"); }
    @font-face { font-family: "Kalam"; font-weight: 700; src: url("assets/fonts/kalam-700.woff2") format("woff2"); }"""

BASE_CSS = f"""
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    .cam {{ position: absolute; inset: 0; transform-origin: 50% 50%; }}
    .cam video {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
    .stk-wrap {{ position: absolute; }}
    .stk {{ display: inline-block; background: {C['paper']}; color: {C['ink']}; font-family: "Kalam"; font-weight: 700;
      font-size: 54px; line-height: 1.08; padding: 16px 30px 12px; border-radius: 22px; border: 5px solid {C['ink']};
      box-shadow: 0 8px 0 rgba(0,0,0,.28); transform-origin: 30% 50%; white-space: nowrap; }}
    .chip-wrap {{ position: absolute; left: 56px; top: 196px; }}
    .chip {{ display: flex; align-items: center; gap: 18px; padding: 12px 26px 10px 14px; border-radius: 999px;
      border: 5px solid {C['ink']}; font-family: "Permanent Marker"; font-size: 44px; color: {C['ink']};
      box-shadow: 0 7px 0 rgba(0,0,0,.28); transform-origin: 0% 50%; white-space: nowrap; }}
    .chip .num {{ width: 64px; height: 64px; border-radius: 50%; background: {C['ink']}; color: #fff; display: flex;
      align-items: center; justify-content: center; font-size: 36px; }}
    .chip svg {{ width: 58px; height: 58px; }}
    .flood {{ position: absolute; inset: 0; }}
    .flood-in {{ position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center;
      gap: 18px; border-left: 10px solid {C['ink']}; }}
    .flood-k {{ font-family: "Kalam"; font-weight: 700; font-size: 64px; color: {C['ink']}; background: #fff; padding: 6px 30px 2px;
      border: 5px solid {C['ink']}; border-radius: 16px; transform: rotate(-3deg); }}
    .flood-t {{ font-family: "Permanent Marker"; font-size: 116px; line-height: 1.02; color: #fff; text-align: center;
      -webkit-text-stroke: 12px {C['ink']}; paint-order: stroke fill; }}
    .flood-in svg {{ width: 170px; height: 170px; }}
    .doodle path, .doodle line {{ fill: none; stroke: {C['spark']}; stroke-width: 11; stroke-linecap: round; }}"""

# ---------- inline icons (simple marker-style SVGs) ----------
S = f'stroke="{C["ink"]}" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"'
ICON = {
    "burger": f'<svg viewBox="0 0 100 100"><path d="M14 46 Q50 6 86 46 Z" fill="#F4A940" {S}/><rect x="10" y="50" width="80" height="10" rx="5" fill="#6BCB4A" {S}/><rect x="12" y="62" width="76" height="12" rx="6" fill="#8B4A2B" {S}/><path d="M14 78 H86 Q84 92 70 92 H30 Q16 92 14 78 Z" fill="#F4A940" {S}/></svg>',
    "book": f'<svg viewBox="0 0 100 100"><path d="M50 26 Q30 14 10 20 V82 Q30 76 50 88 Z" fill="#fff" {S}/><path d="M50 26 Q70 14 90 20 V82 Q70 76 50 88 Z" fill="{C["blue"]}" {S}/><line x1="20" y1="40" x2="40" y2="44" {S}/><line x1="20" y1="54" x2="40" y2="58" {S}/></svg>',
    "laptop": f'<svg viewBox="0 0 100 100"><rect x="18" y="20" width="64" height="44" rx="5" fill="#9AD0F5" {S}/><path d="M8 72 H92 L86 84 H14 Z" fill="#ddd" {S}/></svg>',
    "camera": f'<svg viewBox="0 0 100 100"><path d="M12 34 H32 L38 24 H62 L68 34 H88 V80 H12 Z" fill="#fff" {S}/><circle cx="50" cy="56" r="16" fill="{C["blue"]}" {S}/></svg>',
    "bulb": f'<svg viewBox="0 0 100 100"><path d="M50 10 A28 28 0 0 0 32 60 Q38 66 38 74 H62 Q62 66 68 60 A28 28 0 0 0 50 10 Z" fill="{C["spark"]}" {S}/><line x1="40" y1="82" x2="60" y2="82" {S}/><line x1="43" y1="91" x2="57" y2="91" {S}/></svg>',
    "people": f'<svg viewBox="0 0 100 100"><circle cx="34" cy="34" r="13" fill="#fff" {S}/><circle cx="66" cy="34" r="13" fill="#fff" {S}/><path d="M12 84 Q14 54 34 54 Q50 54 50 70 Q50 54 66 54 Q86 54 88 84 Z" fill="{C["blue"]}" {S}/></svg>',
    "battery": f'<svg viewBox="0 0 140 70"><rect x="6" y="8" width="112" height="54" rx="10" fill="#fff" {S}/><rect x="118" y="24" width="14" height="22" rx="4" fill="{C["ink"]}"/><rect x="16" y="18" width="18" height="34" rx="4" fill="#E5383B"/></svg>',
    "check": f'<svg viewBox="0 0 100 100"><rect x="8" y="8" width="84" height="84" rx="16" fill="{C["green"]}" {S}/><path d="M26 52 L44 70 L76 32" fill="none" stroke="#fff" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "heart": f'<svg viewBox="0 0 100 100"><path d="M50 86 L16 52 A20 20 0 0 1 50 22 A20 20 0 0 1 84 52 Z" fill="{C["pink"]}" {S}/></svg>',
    "play": f'<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="42" fill="#fff" {S}/><path d="M40 30 L72 50 L40 70 Z" fill="{C["ink"]}"/></svg>',
    "bubble": f'<svg viewBox="0 0 100 100"><path d="M14 18 H86 Q92 18 92 24 V64 Q92 70 86 70 H44 L24 88 L28 70 H14 Q8 70 8 64 V24 Q8 18 14 18 Z" fill="#fff" {S}/><circle cx="32" cy="44" r="5" fill="{C["ink"]}"/><circle cx="50" cy="44" r="5" fill="{C["ink"]}"/><circle cx="68" cy="44" r="5" fill="{C["ink"]}"/></svg>',
}

def spark(id_, x, y, rot=0, scale=1.0):
    """Three short marker strokes radiating, drawn on via stroke-dashoffset."""
    return (f'<svg id="{id_}" class="doodle" data-layout-ignore viewBox="0 0 120 120" style="position:absolute;left:{x}px;top:{y}px;'
            f'width:{int(120*scale)}px;height:{int(120*scale)}px;z-index:45;transform:rotate({rot}deg)">'
            '<line x1="20" y1="60" x2="52" y2="60" pathLength="1"/><line x1="30" y1="22" x2="56" y2="44" pathLength="1"/>'
            '<line x1="30" y1="98" x2="56" y2="76" pathLength="1"/></svg>')

def arrow(id_, x, y, w, h, d, color=None, rot=0):
    col = color or C["paper"]
    return (f'<svg id="{id_}" data-layout-ignore viewBox="0 0 200 200" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:45;transform:rotate({rot}deg)">'
            f'<path d="{d}" pathLength="1" fill="none" stroke="{C["ink"]}" stroke-width="20" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" pathLength="1" fill="none" stroke="{col}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></svg>')

def video(sid, i, shot, start, dur, rate=None):
    r = f' data-playback-rate="{rate}"' if rate else ""
    return (f'<div class="cam" id="{sid}-cam{i}" style="z-index:{i}"><video id="{sid}-v{i}" class="clip" src="assets/shots/{shot}.mp4" '
            f'data-start="{start}" data-duration="{dur}" data-media-start="0" data-hf-media-start-basis="local" data-track-index="0"{r} data-has-audio="true" '
            f'data-volume="0.4" data-fade-in="0.03" data-fade-out="0.03" playsinline></video></div>')

def sticker(sid, i, text, start, dur, x, y, rot=-3, size=None, extra=""):
    fs = f' style="font-size:{size}px"' if size else ""
    return (f'<div id="{sid}-s{i}" class="clip stk-wrap" data-start="{start}" data-duration="{dur}" data-track-index="2" '
            f'data-rot="{rot}" style="left:{x}px;top:{y}px;z-index:50"><div class="stk"{fs}>{text}</div>{extra}</div>')

STK_JS = """
    document.querySelectorAll('#root .stk-wrap').forEach((w) => {
      const s = +w.dataset.start, d = +w.dataset.duration, r = +w.dataset.rot, el = w.querySelector('.stk');
      tl.fromTo(el, { scale: 0.35, rotation: r - 12, opacity: 0 }, { scale: 1, rotation: r, opacity: 1, duration: 0.34, ease: 'back.out(2.2)' }, s);
      tl.to(el, { scale: 0.85, opacity: 0, duration: 0.12, ease: 'power2.in' }, s + d - 0.13);
    });"""

def punch(sid, i, start, frm=1.1):
    return f"tl.fromTo('#{sid}-cam{i}', {{ scale: {frm} }}, {{ scale: 1, duration: 0.42, ease: 'expo.out' }}, {start});"

def draw(sel, t, dur=0.22):
    return f"tl.fromTo('{sel}', {{ strokeDasharray: 1, strokeDashoffset: 1 }}, {{ strokeDashoffset: 0, duration: {dur}, stagger: 0.05, ease: 'power2.out' }}, {t});"

def scene(sid, dur, body, js, css="", root_bg=""):
    html = f"""<template>
  <style>{FONTS}{BASE_CSS}{css}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920" data-duration="{dur}">
{body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});{js}
    window.__timelines["{sid}"] = tl;
  </script>
</template>
"""
    (P / "compositions" / f"{sid}.html").write_text(html)

def section(sid, color, num, title, icon, shots, stickers, extra_body="", extra_js="", dur=None):
    """A character section: colour-flood title card, header chip, shots with punch-ins, stickers."""
    body, js = [], []
    t = 0.0
    for i, (shot, d) in enumerate(shots, 1):
        body.append("    " + video(sid, i, shot, round(t, 2), d))
        js.append("    " + punch(sid, i, round(t, 2), 1.12 if i > 1 else 1.0))
        t += d
    dur = dur or round(t, 2)
    body.append(f'''    <div id="{sid}-flood" class="clip flood" data-start="0" data-duration="0.82" data-track-index="3" style="z-index:80">
      <div class="flood-in" style="background:{color}">
        <div class="flood-k">INTERN {num}</div>
        <div class="flood-t">{title.replace(" ", "<br>", 1) if len(title) > 14 else title}</div>
        {ICON[icon]}
      </div>
    </div>
    <div id="{sid}-chip" class="clip chip-wrap" data-start="0.72" data-duration="{round(dur - 0.72, 2)}" data-track-index="1" style="z-index:60">
      <div class="chip" style="background:{color}"><span class="num">{num}</span>{title}{ICON[icon]}</div>
    </div>''')
    for i, s in enumerate(stickers, 1):
        body.append("    " + sticker(sid, i, *s))
    body.append(extra_body)
    js.append(f"""    tl.fromTo('#{sid}-flood .flood-in', {{ x: 1100 }}, {{ x: 0, duration: 0.2, ease: 'power3.out' }}, 0);
    tl.fromTo('#{sid}-flood .flood-k', {{ scale: 0.5, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.25, ease: 'back.out(2)' }}, 0.12);
    tl.fromTo('#{sid}-flood .flood-t', {{ scale: 1.3, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.22, ease: 'expo.out' }}, 0.18);
    tl.fromTo('#{sid}-flood svg', {{ scale: 0, rotation: -30 }}, {{ scale: 1, rotation: 0, duration: 0.3, ease: 'back.out(2.5)' }}, 0.26);
    tl.to('#{sid}-flood .flood-in', {{ y: -1960, duration: 0.24, ease: 'power3.in' }}, 0.56);
    tl.fromTo('#{sid}-chip .chip', {{ x: -700 }}, {{ x: 0, duration: 0.36, ease: 'expo.out' }}, 0.72);
    tl.to('#{sid}-chip .chip', {{ x: -760, duration: 0.18, ease: 'power3.in' }}, {round(dur - 0.2, 2)});""")
    js.append(STK_JS)
    js.append(extra_js)
    scene(sid, dur, "\n".join(body), "\n" + "\n".join(js))
    return dur

# ================= SCENES =================
# 1 hook ---------------------------------------------------------------
scene("hook", 2.5, f"""    {video("hook", 1, "a1", 0, 2.5)}
    <div id="hook-scrim" style="position:absolute;inset:0;background:radial-gradient(120% 60% at 50% 22%, rgba(0,0,0,.55), rgba(0,0,0,0) 70%);z-index:5"></div>
    <div id="hook-text" style="position:absolute;left:70px;top:300px;width:900px;z-index:20">
      <div id="hook-pov" style="font-family:'Permanent Marker';font-size:190px;line-height:1;color:#fff;-webkit-text-stroke:16px {C['ink']};paint-order:stroke fill;transform:rotate(-4deg)">POV:</div>
      <div id="hook-line" style="margin-top:26px;font-family:'Kalam';font-weight:700;font-size:84px;line-height:1.12;color:#fff;-webkit-text-stroke:12px {C['ink']};paint-order:stroke fill">
        Bila <span id="hook-hl" style="position:relative;display:inline-block"><span id="hook-hl-bg" style="position:absolute;left:-10px;right:-10px;top:14px;bottom:4px;background:{C['spark']};border-radius:10px;transform-origin:0 50%;z-index:-1"></span>3 intern</span><br>pergi event<br>yang sama...
      </div>
    </div>
    {spark("hook-spark", 640, 250, -10, 1.3)}""",
"""
    tl.fromTo('#hook-hl-bg', { scaleX: 0 }, { scaleX: 1, duration: 0.28, ease: 'power3.out' }, 0.5);
    """ + draw("#hook-spark line", 0.15) + """
    tl.fromTo('#hook-cam1', { scale: 1.0 }, { scale: 1.06, duration: 2.5, ease: 'none' }, 0);
    tl.to('#hook-text', { y: -120, opacity: 0, duration: 0.18, ease: 'power3.in' }, 2.3);""",
css="\n    #hook-line { isolation: isolate; }")

# 2 intro --------------------------------------------------------------
cards = [("food", C["pink"], "Intern 01", "The Food<br>Hunter", -6, 70),
         ("learn", C["blue"], "Intern 02", "The<br>Intellectual", 2, 395),
         ("work", C["yellow"], "Intern 03", "The Corporate<br>Survivor", -3, 720)]
card_html = "\n".join(f'''    <div id="intro-card{i}" class="intro-card" data-rot="{r}" style="left:{x}px;top:{850 + (i % 2) * 30}px;z-index:{30 + i}">
      <div class="pol" style="border-color:{col}"><img src="assets/stills/{img}.jpg" alt=""></div>
      <div class="lab" style="background:{col}"><b>{k}</b><br>{t}</div>
    </div>''' for i, (img, col, k, t, r, x) in enumerate(cards, 1))
scene("intro", 2.5, f"""    {video("intro", 1, "b1", 0, 2.5)}
    <div style="position:absolute;inset:0;background:rgba(10,10,14,.58);z-index:5"></div>
    <div id="intro-t1" class="big" style="top:300px;left:70px;background:{C['blue']};transform:rotate(-3deg)">3 intern.</div>
    <div id="intro-t2" class="big" style="top:470px;left:300px;background:{C['pink']};transform:rotate(2deg)">1 event.</div>
    <div id="intro-sub" style="position:absolute;top:668px;left:70px;width:860px;text-align:center;font-family:'Kalam';font-weight:700;font-size:48px;line-height:1.15;color:#fff;z-index:20">Same place. Different missions.<br>Same chaos.</div>
{card_html}
    {spark("intro-spark", 830, 280, 200, 1.1)}""",
"""
    tl.fromTo('#intro-t1', { scale: 1.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.24, ease: 'expo.out' }, 0.08);
    tl.fromTo('#intro-t2', { scale: 1.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.24, ease: 'expo.out' }, 0.33);
    tl.fromTo('#intro-sub', { opacity: 0, filter: 'blur(6px)' }, { opacity: 1, filter: 'blur(0px)', duration: 0.18 }, 0.6);
    document.querySelectorAll('#root .intro-card').forEach((c, i) => {
      tl.fromTo(c, { y: 700, rotation: +c.dataset.rot * 3 }, { y: 0, rotation: +c.dataset.rot, duration: 0.42, ease: 'back.out(1.4)' }, 0.72 + i * 0.15);
    });
    """ + draw("#intro-spark line", 0.4) + """
    tl.to('#root .intro-card, #intro-t1, #intro-t2, #intro-sub', { opacity: 0, y: '-=80', duration: 0.15, ease: 'power2.in' }, 2.33);""",
css=f"""
    .big {{ position: absolute; z-index: 20; font-family: "Permanent Marker"; font-size: 132px; line-height: 1.05; color: #fff;
      -webkit-text-stroke: 12px {C['ink']}; paint-order: stroke fill; padding: 4px 34px 0; border: 6px solid {C['ink']}; border-radius: 20px; }}
    .intro-card {{ position: absolute; width: 280px; }}
    .pol {{ background: #fff; border: 10px solid; border-radius: 26px; padding: 0; overflow: hidden; height: 330px;
      box-shadow: 0 10px 0 rgba(0,0,0,.3); outline: 5px solid {C['ink']}; }}
    .pol img {{ width: 100%; height: 100%; object-fit: cover; }}
    .lab {{ margin: -26px 8px 0; position: relative; border: 5px solid {C['ink']}; border-radius: 18px; text-align: center;
      font-family: "Kalam"; font-weight: 700; font-size: 34px; line-height: 1.05; color: {C['ink']}; padding: 10px 6px 6px; }}
    .lab b {{ font-size: 28px; }}""")

# 3 mission start -------------------------------------------------------
scene("mission", 1.5, f"""    {video("mission", 1, "c1", 0, 1.5, rate=1.25)}
    <div id="mission-flash" style="position:absolute;inset:0;background:#fff;z-index:40;opacity:0"></div>
    <div id="mission-box" style="position:absolute;left:110px;top:640px;width:860px;z-index:30;text-align:center">
      <div id="mission-slab" style="display:inline-block;background:#fff;border:7px solid {C['ink']};border-radius:20px;padding:14px 40px 4px;
        font-family:'Permanent Marker';font-size:112px;color:{C['ink']};box-shadow:0 12px 0 rgba(0,0,0,.35);transform:rotate(-4deg)">MISSION START!</div>
      <div id="mission-play" style="width:170px;height:170px;margin:34px auto 0">{ICON['play']}</div>
      <div id="mission-sub" style="margin-top:18px;font-family:'Kalam';font-weight:700;font-size:56px;color:#fff;-webkit-text-stroke:10px {C['ink']};paint-order:stroke fill">Let's go!</div>
    </div>
    {spark("mission-spark", 60, 560, -20, 1.2)}{spark("mission-spark2", 880, 1010, 160, 1.0)}""",
"""
    tl.fromTo('#mission-flash', { opacity: 0.9 }, { opacity: 0, duration: 0.2, ease: 'power2.out' }, 0);
    tl.fromTo('#mission-slab', { scale: 2.2, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.2, ease: 'power4.out' }, 0);
    tl.fromTo('#mission-play', { scale: 0 }, { scale: 1, duration: 0.3, ease: 'back.out(2.5)' }, 0.16);
    tl.fromTo('#mission-sub', { opacity: 0, filter: 'blur(6px)' }, { opacity: 1, filter: 'blur(0px)', duration: 0.15 }, 0.3);
    """ + draw("#mission-spark line, #mission-spark2 line", 0.12) + """
    tl.to('#mission-box', { x: -1100, duration: 0.16, ease: 'power3.in' }, 1.34);""")

# 4 food hunter -----------------------------------------------------------
food_dur = section("food", C["pink"], "01", "The Food Hunter", "burger",
    [("d1", 2.3), ("d2", 1.7), ("d3", 1.7), ("d4", 0.6), ("d5", 1.6)],
    [("Booth? Nanti dulu...", 0.85, 1.45, 70, 1120, -4),
     ("Food hunting in progress...", 2.45, 1.55, 70, 1150, 3),
     ("Researching local cuisine", 4.15, 1.55, 70, 1150, -2),
     ("Mission 1:<br>Completed!", 6.4, 1.5, 560, 560, 6, 64)],
    extra_body=f"""    {arrow("food-arrow", 560, 1000, 300, 260, "M20 160 Q100 160 150 60 M120 72 L150 60 L160 96", rot=0)}
    <div id="food-check" style="position:absolute;left:470px;top:530px;width:120px;height:120px;z-index:55">{ICON['check']}</div>
    <div id="food-heart" style="position:absolute;left:760px;top:1060px;width:110px;height:110px;z-index:55">{ICON['heart']}</div>
    {spark("food-spark", 860, 470, 30, 1.0)}""",
    extra_js="""
    tl.fromTo('#food-arrow path', { strokeDasharray: 1, strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.3, ease: 'power2.out' }, 1.0);
    tl.to('#food-arrow', { opacity: 0, duration: 0.1 }, 2.2);
    tl.fromTo('#food-heart', { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.3, ease: 'back.out(3)' }, 4.35);
    tl.to('#food-heart', { scale: 0, duration: 0.1 }, 5.6);
    tl.fromTo('#food-check', { scale: 0, rotation: -40 }, { scale: 1, rotation: -8, duration: 0.32, ease: 'back.out(2.6)' }, 6.5);
    """ + draw("#food-spark line", 6.55))

# 5 the intellectual -------------------------------------------------------
learn_dur = section("learn", C["blue"], "02", "The Intellectual", "book",
    [("e1", 2.3), ("e2", 1.7), ("e3", 1.7), ("e4", 1.7)],
    [("Exploring meaningful booths...", 0.85, 1.45, 70, 1150, -3),
     ("Asking questions...", 2.45, 1.55, 70, 1150, 2),
     ("Knowledge acquired <span style='color:#1E8C55'>+10</span>", 4.15, 1.55, 70, 1150, -3),
     ("Networking mode: <span style='color:#1E8C55'>ON</span>", 5.85, 1.55, 70, 1150, 2)],
    extra_body=f"""    <div id="learn-q" class="qm" style="left:620px;top:1000px">?</div><div id="learn-q2" class="qm" style="left:740px;top:930px;font-size:120px">?</div>
    <div id="learn-bulb" style="position:absolute;left:790px;top:1010px;width:130px;height:130px;z-index:55">{ICON['bulb']}</div>
    <div id="learn-ppl" style="position:absolute;left:800px;top:1020px;width:120px;height:120px;z-index:55">{ICON['people']}</div>""",
    extra_js="""
    tl.fromTo('#learn-q, #learn-q2', { scale: 0, rotation: -30 }, { scale: 1, rotation: 0, duration: 0.3, stagger: 0.12, ease: 'back.out(3)' }, 2.6);
    tl.to('#learn-q, #learn-q2', { opacity: 0, duration: 0.1 }, 3.9);
    tl.fromTo('#learn-bulb', { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.3, ease: 'back.out(3)' }, 4.3);
    tl.to('#learn-bulb', { opacity: 0, duration: 0.1 }, 5.6);
    tl.fromTo('#learn-ppl', { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.3, ease: 'back.out(3)' }, 6.0);""")
for f in [P / "compositions" / "learn.html"]:
    f.write_text(f.read_text().replace("  </style>", f"""    .qm {{ position: absolute; z-index: 55; font-family: "Permanent Marker"; font-size: 150px; color: #fff; -webkit-text-stroke: 12px {C['ink']}; paint-order: stroke fill; }}
  </style>""", 1))

# 6 the corporate survivor ---------------------------------------------------
work_dur = section("work", C["yellow"], "03", "The Corporate Survivor", "laptop",
    [("f1", 2.3), ("f2", 1.7), ("f3", 1.7), ("f4", 3.1)],
    [("Carrying this...", 0.85, 1.45, 70, 1150, -3),
     ("Shooting that...", 2.45, 1.55, 70, 1150, 3),
     ("Lunch break? What is that...", 4.05, 1.65, 70, 1150, -2),
     ("Clock in: <span style='color:#1E8C55'>YES</span>", 5.85, 2.9, 70, 820, -3),
     ("Clock out: <span style='color:#C1121F'>UNAVAILABLE</span>", 6.3, 2.45, 70, 960, 2),
     ("Work-life balance<br>has left the chat.", 6.75, 2.05, 70, 1100, -2, 50)],
    extra_body=f"""    <div id="work-cam-ico" style="position:absolute;left:560px;top:1120px;width:130px;height:130px;z-index:55">{ICON['camera']}</div>
    <div id="work-batt" style="position:absolute;left:640px;top:640px;width:220px;height:110px;z-index:55">{ICON['battery']}</div>""",
    extra_js="""
    tl.fromTo('#work-cam-ico', { scale: 0, rotation: 30 }, { scale: 1, rotation: 8, duration: 0.3, ease: 'back.out(3)' }, 2.6);
    tl.to('#work-cam-ico', { opacity: 0, duration: 0.1 }, 3.9);
    tl.fromTo('#work-batt', { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.3, ease: 'back.out(3)' }, 5.95);
    tl.fromTo('#work-batt rect:nth-child(3)', { opacity: 1 }, { opacity: 0.15, duration: 0.12, repeat: 5, yoyo: true, ease: 'none' }, 6.4);
    tl.to('#work-batt', { opacity: 0, duration: 0.12 }, 8.6);""")

# 7 chaotic montage -----------------------------------------------------------
labels = [("EAT", C["pink"]), ("LEARN", C["blue"]), ("WORK", C["yellow"])] * 3
gb, gj = [], []
for i in range(1, 9):
    t = round((i - 1) * 0.5, 2)
    lab, col = labels[i - 1]
    if i == 8:
        lab, col = "REPEAT", C["mint"]
    gb.append("    " + video("mont", i, f"g{i}", t, 0.5))
    side = 70 if i % 2 else 600
    gb.append(f'    <div id="mont-l{i}" class="clip" data-start="{t}" data-duration="0.5" data-track-index="2" style="position:absolute;left:{side}px;top:1170px;z-index:50">'
              f'<div class="tag" style="background:{col}">{lab}</div></div>')
    gj.append(f"    tl.fromTo('#mont-cam{i}', {{ scale: 1.18, rotation: {(-2, 2)[i % 2]} }}, {{ scale: 1.04, rotation: 0, duration: 0.45, ease: 'expo.out' }}, {t});")
    gj.append(f"    tl.fromTo('#mont-l{i} .tag', {{ scale: 0.4, rotation: -14 }}, {{ scale: 1, rotation: {(-5, 4)[i % 2]}, duration: 0.2, ease: 'back.out(3)' }}, {t});")
scene("montage", 4.0, "\n".join(gb) + f"""
    <div id="mont-pay" class="clip" data-start="1.5" data-duration="2.5" data-track-index="3" style="position:absolute;left:70px;top:560px;width:900px;z-index:70;text-align:center">
      <div id="mont-p1" class="pay" style="color:#fff">Different missions.</div>
      <div id="mont-p2" class="pay" style="color:{C['spark']}">Same energy.</div>
    </div>
    {spark("mont-spark", 30, 470, -30, 1.2)}{spark("mont-spark2", 900, 760, 150, 1.1)}""",
"\n" + "\n".join(gj) + """
    tl.fromTo('#mont-p1', { scale: 1.5, opacity: 0, rotation: -6 }, { scale: 1, opacity: 1, rotation: -4, duration: 0.24, ease: 'expo.out' }, 1.5);
    tl.fromTo('#mont-p2', { scale: 1.5, opacity: 0, rotation: 0 }, { scale: 1, opacity: 1, rotation: 2, duration: 0.24, ease: 'expo.out' }, 1.75);
    """ + draw("#mont-spark line, #mont-spark2 line", 1.85) + """
    tl.to('#mont-pay', { scale: 1.3, opacity: 0, duration: 0.14, ease: 'power3.in' }, 3.84);""",
css=f"""
    .tag {{ font-family: "Permanent Marker"; font-size: 76px; color: {C['ink']}; border: 6px solid {C['ink']}; border-radius: 18px;
      padding: 6px 34px 0; box-shadow: 0 8px 0 rgba(0,0,0,.3); }}
    .pay {{ font-family: "Permanent Marker"; font-size: 120px; line-height: 1.08; -webkit-text-stroke: 14px {C['ink']}; paint-order: stroke fill; }}""")

# 8 finale --------------------------------------------------------------------
scene("finale", 3.1, f"""    {video("finale", 1, "h1", 0, 3.1)}
    <div id="finale-flash" style="position:absolute;inset:0;background:#fff;z-index:40;opacity:0"></div>
    <div id="finale-card" style="position:absolute;left:60px;top:1035px;width:900px;z-index:50">
      <div id="finale-l1" style="display:inline-block;background:#fff;border:6px solid {C['ink']};border-radius:24px;padding:16px 30px 10px;
        font-family:'Kalam';font-weight:700;font-size:54px;line-height:1.08;color:{C['ink']};box-shadow:0 9px 0 rgba(0,0,0,.3);transform:rotate(-2deg)">Same event.<br>Different internship experience.</div>
      <div id="finale-l2" style="margin:18px 0 0 40px;display:inline-flex;align-items:center;gap:14px;background:{C['ink']};border-radius:999px;padding:12px 30px 8px;
        font-family:'Kalam';font-weight:700;font-size:44px;color:#fff;transform:rotate(1.5deg)">Chaotic, but we wouldn't change it <span style="display:inline-block;width:52px;height:52px">{ICON['heart']}</span></div>
    </div>
    {spark("finale-spark", 30, 960, -20, 1.1)}{spark("finale-spark2", 840, 900, 160, 1.0)}""",
"""
    tl.fromTo('#finale-flash', { opacity: 1 }, { opacity: 0, duration: 0.3, ease: 'power2.out' }, 0);
    tl.fromTo('#finale-cam1', { scale: 1.15 }, { scale: 1, duration: 0.6, ease: 'expo.out' }, 0);
    tl.fromTo('#finale-l1', { y: 300, rotation: -10, opacity: 0 }, { y: 0, rotation: -2, opacity: 1, duration: 0.38, ease: 'back.out(1.6)' }, 0.15);
    tl.fromTo('#finale-l2', { scale: 0.4, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.3, ease: 'back.out(2.4)' }, 0.55);
    """ + draw("#finale-spark line, #finale-spark2 line", 0.4) + """
    tl.to('#finale-card', { y: 260, opacity: 0, duration: 0.16, ease: 'power3.in' }, 2.92);""")

# 9 CTA -----------------------------------------------------------------------
scene("cta", 2.8, f"""    {video("cta", 1, "i1", 0, 2.8)}
    <div style="position:absolute;inset:0;background:rgba(10,10,14,.6);z-index:5"></div>
    <div id="cta-tag" style="position:absolute;left:110px;top:560px;width:820px;z-index:30;text-align:center">
      <div id="cta-q" style="display:inline-block;background:#fff;border:7px solid {C['ink']};border-radius:26px;padding:22px 44px 10px;
        font-family:'Permanent Marker';font-size:104px;line-height:1.05;color:{C['ink']};box-shadow:0 12px 0 rgba(0,0,0,.35);transform:rotate(-5deg)">Which intern<br>are you?</div>
    </div>
    <div id="cta-c" style="position:absolute;left:150px;top:960px;z-index:30;display:flex;align-items:center;gap:20px;background:{C['ink']};
      border:5px solid #fff;border-radius:999px;padding:16px 40px 10px;font-family:'Kalam';font-weight:700;font-size:62px;color:#fff;transform:rotate(2deg)">
      Comment below! <span style="display:inline-block;width:80px;height:80px">{ICON['bubble']}</span></div>
    {arrow("cta-arrow", 640, 1060, 300, 260, "M30 20 Q150 30 160 150 M126 124 L160 150 L182 112", color=C['spark'])}
    {spark("cta-spark", 40, 500, -20, 1.2)}{spark("cta-spark2", 870, 480, 200, 1.1)}
    <div id="cta-cards" style="position:absolute;left:0;top:1180px;width:1080px;z-index:20">
      <div class="mini" style="left:120px;background:{C['pink']};transform:rotate(-6deg)">01</div>
      <div class="mini" style="left:300px;background:{C['blue']};transform:rotate(3deg)">02</div>
      <div class="mini" style="left:480px;background:{C['yellow']};transform:rotate(-2deg)">03</div>
    </div>""",
"""
    tl.fromTo('#cta-q', { scale: 1.8, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.26, ease: 'expo.out' }, 0.12);
    tl.fromTo('#cta-c', { y: 160, opacity: 0 }, { y: 0, opacity: 1, duration: 0.34, ease: 'back.out(1.8)' }, 0.5);
    tl.fromTo('#cta-arrow path', { strokeDasharray: 1, strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.32, ease: 'power2.out' }, 0.75);
    tl.fromTo('#cta-cards .mini', { y: 200, opacity: 0 }, { y: 0, opacity: 1, duration: 0.3, stagger: 0.08, ease: 'back.out(2)' }, 0.55);
    """ + draw("#cta-spark line, #cta-spark2 line", 0.3),
css=f"""
    .mini {{ position: absolute; top: 0; width: 130px; height: 120px; display: flex; align-items: center; justify-content: center;
      font-family: "Permanent Marker"; font-size: 64px; color: {C['ink']}; border: 6px solid {C['ink']}; border-radius: 20px; box-shadow: 0 8px 0 rgba(0,0,0,.3); }}""")

# ================= ROOT =================
order = [("hook", 2.5), ("intro", 2.5), ("mission", 1.5), ("food", food_dur), ("learn", learn_dur),
         ("work", work_dur), ("montage", 4.0), ("finale", 3.1), ("cta", 2.8)]
starts, t = {}, 0.0
for sid, d in order:
    starts[sid] = round(t, 2); t += d
TOTAL = round(t, 2)

def at(sid, local):
    return round(starts[sid] + local, 3)

# (name, file, visual moment T, peak offset, volume)
DUR = {"pop": 0.72, "whoosh": 0.575, "whoosh-cinematic": 5.544, "impact-bass-1": 2.116, "impact-bass-2": 2.592, "sparkle": 1.802,
       "ping": 1.32, "error": 1.62, "notification": 2.456, "glitch-1": 2.638, "click-soft": 0.366}
PEAK = {"pop": 0.12, "whoosh": 0.162, "whoosh-cinematic": 2.503, "impact-bass-1": 0.073, "impact-bass-2": 1.986,
        "sparkle": 0.027, "ping": 0.324, "error": 0.745, "notification": 0.229, "glitch-1": 0.82, "click-soft": 0.073}
cues = [
    ("whoosh", at("hook", 0.5), 0.3),
    ("whoosh", at("intro", 0), 0.45), ("pop", at("intro", 0.1), 0.6), ("pop", at("intro", 0.35), 0.55),
    ("click-soft", at("intro", 0.95), 0.7), ("click-soft", at("intro", 1.1), 0.7), ("click-soft", at("intro", 1.25), 0.7),
    ("impact-bass-1", at("mission", 0), 0.5),
    ("whoosh-cinematic", at("food", 0.1), 0.4),
    ("pop", at("food", 0.92), 0.55), ("pop", at("food", 2.52), 0.55), ("pop", at("food", 4.22), 0.55),
    ("pop", at("food", 6.47), 0.55), ("sparkle", at("food", 6.55), 0.45),
    ("whoosh", at("learn", 0.1), 0.45),
    ("pop", at("learn", 0.92), 0.55), ("pop", at("learn", 2.52), 0.55), ("ping", at("learn", 4.3), 0.6), ("pop", at("learn", 5.92), 0.55),
    ("whoosh-cinematic", at("work", 0.1), 0.4),
    ("pop", at("work", 0.92), 0.55), ("pop", at("work", 2.52), 0.55), ("pop", at("work", 4.12), 0.55),
    ("pop", at("work", 5.92), 0.55), ("error", at("work", 6.37), 0.7), ("pop", at("work", 6.82), 0.55),
    ("glitch-1", at("montage", 0), 0.35),
] + [("click-soft", at("montage", i * 0.5), 0.5) for i in range(1, 8)] + [
    ("whoosh", at("montage", 1.5), 0.45),
    ("impact-bass-2", at("finale", 0), 0.55), ("sparkle", at("finale", 0.2), 0.4),
    ("whoosh", at("cta", 0), 0.45), ("pop", at("cta", 0.18), 0.6), ("notification", at("cta", 0.55), 0.45),
]
audio = []
for n, (name, T, vol) in enumerate(cues, 1):
    start = round(T + 1 / 30 - PEAK[name], 3)
    media_start = 0.0
    if start < 0:
        media_start, start = -start, 0.0
    ms = f' data-media-start="{media_start:.3f}"' if media_start else ""
    audio.append(f'      <audio id="sfx{n:02d}" class="clip" src="assets/sfx/{name}.mp3" data-start="{start}" data-duration="{round(min(DUR[name] - media_start, TOTAL - start), 3)}"{ms} data-track-index="{20 + n % 6}" data-volume="{vol}"></audio>')

hosts = "\n".join(f'''      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{starts[sid]}"
        data-duration="{d}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>''' for sid, d in order)

index = f"""<!doctype html>
<html lang="ms" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #111; }}
      #root {{ width: 100%; height: 100%; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920" data-motion-blur="on">
{hosts}
      <!-- Sound effects (Pixabay licence, see assets/sfx/CREDITS.md). Background music: add <audio id="bgm"> here. -->
{chr(10).join(audio)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
(P / "index.html").write_text(index)
print("total", TOTAL, starts)
