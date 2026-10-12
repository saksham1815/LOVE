"""
A Birthday Love Letter, as a website.

    pip install "streamlit>=1.40" pillow
    streamlit run app.py

Keep your pictures in a folder called  images/  next to this file, then list the
file names in the  ✏️ EDIT ME  block below. No uploading needed.
"""
from __future__ import annotations

import base64
import html
import io
import random
from pathlib import Path

import streamlit as st
from PIL import Image, ImageOps

st.set_page_config(
    page_title="Happy Birthday, My Love",
    page_icon="💌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

try:
    _v = tuple(int(x) for x in st.__version__.split(".")[:2])
except Exception:
    _v = (99, 0)
if _v < (1, 40):
    st.error(f"This birthday site needs Streamlit 1.40 or newer (you have {st.__version__}). "
             "Run:  pip install -U streamlit")
    st.stop()

# =============================================================================
# ✏️  EDIT ME — everything personal lives in this block
# =============================================================================

# 📁 Where your pictures live. A folder named "images" next to app.py by default.
#    Want another place?  IMAGES_DIR = Path("C:/Users/me/Pictures/birthday")
try:
    IMAGES_DIR = Path(__file__).resolve().parent / "images"
except NameError:
    IMAGES_DIR = Path.cwd() / "images"

# Every picture below is just a file name inside IMAGES_DIR
# (or a full path like "C:/pics/us.jpg"). A missing file shows a pretty placeholder.
FEATURED_IMAGE = "featured.jpeg"          # the big photo at the top of the gallery
FEATURED_CAPTION = "Our favourite"
FINAL_IMAGE = "final.jpg"                 # the photo on the last screen

GALLERY = [                               # (file name, caption), in the order shown
    ("photo1.jpg", "My favourite day"),
    ("photo2.jpg", "Your beautiful smile"),
    ("photo3.jpg", "A moment I will always remember"),
    ("photo4.jpg", "Just us being us"),
    ("photo5.jpg", "Our little adventure"),
    ("photo6.jpg", "Every picture, a piece of my heart"),
]
# Tip: set GALLERY = [] to automatically show every image found in the folder.

HER_NAME = "Rudie"                      # "Happy Birthday, <name>"
MY_NAME = "You know me , don't you?"         # signs the letter

HERO_EYEBROW = "A little celebration, just for you"
HERO_SCRIPT = "To my favourite person in the entire universe…"
HERO_SUBTITLE = ("Today is all about you, your beautiful smile, "
                 "and the happiness you bring into my world.")
SURPRISE_MESSAGE = ("Surprise! I made you something small, with a lot of love in it. "
                    "Take your time, scroll slowly, and smile a little. 💗")

GALLERY_TITLE = "Our Little World 📸"
GALLERY_SUBTITLE = "Every picture holds a little piece of my heart."
DEFAULT_CAPTIONS = [
    "My favourite day",
    "Your beautiful smile",
    "A moment I will always remember",
    "Just us being us",
    "Our little adventure",
    "Every picture, a piece of my heart",
]

LETTER_GREETING = "Hello Madam ji,"
LETTER_PARAGRAPHS = [
    "Happy Birthday to the girl who somehow managed to turn poora Noida into our personal date spot. 😂❤️ At this point, I think we’ve explored half the city together, and honestly, I wouldn’t mind getting lost in the other half with you too.",

    "From our DLF Sector 18 adventures to watching Project Hail Mary together, it’s funny how even the most ordinary plans become memories I end up keeping close. Matlab plan kuch bhi ho, tum saath ho toh review automatically 5 stars. ⭐",

    "And then there’s you being you — thodi witty, thodi unpredictable, and occasionally so annoying that I have to question my life choices. 🙄❤️ But then you smile, and unfortunately for me, my entire argument loses its credibility. Very unfair behaviour, honestly.",

    "I still think about that sunflower gift. 🌻 It was such a little thing, but somehow it reminds me of you — bright, warm, and capable of making an ordinary day feel a little more special.",

    "I love that we have our own little collection of memories — the places we’ve wandered around, the movies we’ve watched, the random conversations, the silly moments, and all the things that probably wouldn't make sense to anyone else. But that's kind of the point, na? They're ours.",

    "I hope this year gives you a hundred reasons to laugh, a thousand reasons to be proud of yourself, and all the happiness you deserve. I hope you chase every dream you have, keep being your wonderfully witty self, and never forget how special you are — even on the days when you refuse to admit it.",

    "And haan, birthday girl, don't let all this sweetness get to your head. You're still the same girl who i am gonna ragebait you. And in future i will gonna ragebait you bad. Probably. 😌",
]
LETTER_CLOSING = "With all my love,"

QUOTES = [
    "In a world full of temporary things, you are my favourite forever.",
    "You make my ordinary days feel like my favourite memories.",
    "If happiness had a favourite face, mine would look a lot like yours.",
    "You deserve all the love you so effortlessly give to the world.",
    "My favourite place will always be wherever I get to be with you.",
    "Of all the beautiful things life has given me, meeting you is one of my favourites.",
]

WISH_TEXT = ("May this new chapter bring you beautiful surprises, peaceful days, exciting "
             "adventures, endless laughter, and every little thing your heart has been wishing for.")
WISH_CELEBRATION = ("The world became a little more beautiful the day you were born. "
                    "Happy Birthday, sweetheart! ❤️")
NOTE_IDLE = "Close your eyes, make a wish, then blow out the candles."
NOTE_OUT = "Wish made… I hope every bit of it comes true ✨"
NOTE_CUT = "The first slice is yours 🍰💗"

# "photo": None = text only, or a file name from your images folder, e.g. "photo2.jpg".
TIMELINE = [
    {"title": "The Beginning",
     "text": "The start of something that became so special to me.", "photo": None},
    {"title": "Our Little Adventures",
     "text": "The moments when we laughed, explored, and made memories together.", "photo": None},
    {"title": "The Everyday Magic",
     "text": "All those little conversations and ordinary days that mean more than they seem.", "photo": None},
    {"title": "Today and Everything Ahead",
     "text": "Another birthday to celebrate you, with so many beautiful memories still waiting for us.",
     "photo": None},
]

REASONS = [
    ("🌸", "Your smile", "It can turn my whole day around without you even trying."),
    ("🤍", "Your kindness", "The way you care for people quietly and completely."),
    ("😂", "The way you make me laugh", "Even on the days I forgot how."),
    ("💗", "Your beautiful heart", "The softest, strongest thing I know."),
    ("🧸", "The little things you remember", "Proof that you really listen."),
    ("✨", "You make ordinary moments special", "Even a boring Tuesday feels like a date."),
    ("🌷", "Your strength", "Even on the difficult days, you keep going."),
    ("💌", "Simply being yourself", "Never change that. Not one bit."),
]

FINAL_TITLE = "Happy Birthday, My Forever Favourite ❤️"
FINAL_PARAGRAPHS = [
    "If I could make one wish for your birthday, it would be that you always feel as loved, "
    "appreciated, and special as you truly are.",
    "Here's to your dreams, your happiness, your beautiful smile, and all the wonderful moments "
    "still waiting for you.",
    "I love you, birthday girl. Today, tomorrow, and in all the little moments in between.",
]
HUG_MESSAGE = ("Sending you the biggest virtual hug and a million kisses. Consider this your "
               "birthday hug until I can give you a real one. ❤️")
FOOTER_LINE = "Made with love, just for you. 💗"

EXTS = {".jpg", ".jpeg", ".png", ".webp"}

# =============================================================================
# Helpers
# =============================================================================


def esc(text) -> str:
    return html.escape(str(text), quote=True)


def clean(markup: str) -> str:
    """Strip indentation + blank lines so Streamlit's markdown never treats HTML as code."""
    return "\n".join(line.strip() for line in markup.splitlines() if line.strip())


def render(markup: str) -> None:
    st.markdown(clean(markup), unsafe_allow_html=True)


@st.cache_data(show_spinner=False, max_entries=64)
def to_data_uri(raw: bytes) -> str:
    """Resize + embed an image as a data URI (cached, so reruns are cheap)."""
    try:
        img = Image.open(io.BytesIO(raw))
        img = ImageOps.exif_transpose(img)
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGBA")
            bg = Image.new("RGB", img.size, (255, 248, 242))
            bg.paste(img, mask=img.split()[-1])
            img = bg
        else:
            img = img.convert("RGB")
        img.thumbnail((1100, 1100))
        buf = io.BytesIO()
        img.save(buf, "JPEG", quality=84, optimize=True)
        return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception:
        return ""


@st.cache_data(show_spinner=False)
def _load_uri(path_str: str, stamp: int) -> str:
    try:
        return to_data_uri(Path(path_str).read_bytes())
    except OSError:
        return ""


def _find_similar(p: Path):
    """Same name in the same folder, ignoring extension / capitalisation (featured.jpg -> Featured.JPEG)."""
    try:
        for q in p.parent.iterdir():
            if q.is_file() and q.stem.lower() == p.stem.lower() and q.suffix.lower() in EXTS:
                return q
    except OSError:
        pass
    return None


def get_photo(ref):
    """File name (inside IMAGES_DIR) or full path -> {"uri": ...}, or None if missing."""
    if not ref:
        return None
    p = Path(str(ref)).expanduser()
    if not p.is_absolute():
        p = IMAGES_DIR / p
    if not p.is_file():
        p = _find_similar(p) or p
    try:
        uri = _load_uri(str(p), p.stat().st_mtime_ns) if p.is_file() else ""
    except OSError:
        uri = ""
    if not uri:
        print(f"[birthday] image not found or unreadable: {p}")
        return None
    return {"uri": uri}


def gallery_items() -> list:
    """[(photo_or_None, caption), ...] from GALLERY (or every image in the folder if GALLERY is empty)."""
    entries = list(GALLERY)
    if not entries and IMAGES_DIR.is_dir():
        skip = {str(FEATURED_IMAGE).lower(), str(FINAL_IMAGE).lower()}
        entries = [(p.name, "") for p in sorted(IMAGES_DIR.iterdir(), key=lambda q: q.name.lower())
                   if p.is_file() and p.suffix.lower() in EXTS and p.name.lower() not in skip]
    items = []
    for i, e in enumerate(entries):
        name, cap = (e, "") if isinstance(e, str) else (e[0], e[1] if len(e) > 1 else "")
        items.append((get_photo(name), cap or DEFAULT_CAPTIONS[i % len(DEFAULT_CAPTIONS)]))
    return items


def hearts_html(n: int, seed: int, rise: str | None = None) -> str:
    rnd = random.Random(seed)
    glyphs = ["❤", "♡", "❤", "💗"]
    colors = ["#EFA3BB", "#C44569", "#F8D7E5", "#e58aa6"]
    spans = []
    for _ in range(n):
        spans.append(
            f'<span class="hrt" style="--x:{rnd.uniform(2, 96):.1f}%;--s:{rnd.uniform(12, 28):.0f}px;'
            f'--d:{rnd.uniform(12, 22):.1f}s;--dl:-{rnd.uniform(0, 20):.1f}s;--c:{rnd.choice(colors)}">'
            f'{rnd.choice(glyphs)}</span>'
        )
    kind = "local" if rise else "fixed"
    style = f' style="--h:{rise}"' if rise else ""
    return f'<div class="hrt-layer {kind}"{style}>{"".join(spans)}</div>'


def sparks_html(n: int, seed: int) -> str:
    rnd = random.Random(seed)
    return "".join(
        f'<span class="spark" style="top:{rnd.uniform(4, 92):.0f}%;left:{rnd.uniform(3, 95):.0f}%;'
        f'--s:{rnd.uniform(10, 20):.0f}px;--dl:{rnd.uniform(0, 3):.1f}s">✦</span>'
        for _ in range(n)
    )


def confetti_html(seed: int, n: int = 80) -> str:
    rnd = random.Random(seed)
    colors = ["#C44569", "#EFA3BB", "#F8D7E5", "#7A2947", "#ffd7a8", "#ffffff"]
    bits = []
    for _ in range(n):
        kind = "h" if rnd.random() < 0.3 else "c"
        bits.append(
            f'<i class="cf {kind}" style="left:{rnd.uniform(0, 100):.1f}%;--d:{rnd.uniform(3.5, 7):.2f}s;'
            f'--dl:{rnd.uniform(0, 1.2):.2f}s;--s:{rnd.uniform(8, 18):.0f}px;--c:{rnd.choice(colors)};'
            f'--dx:{rnd.uniform(-90, 90):.0f}px;--r:{rnd.uniform(240, 900):.0f}deg"></i>'
        )
    return f'<div class="cf-layer">{"".join(bits)}</div>'


def paragraphs(items) -> str:
    return "".join(f"<p>{esc(p)}</p>" for p in items)


# =============================================================================
# Styles
# =============================================================================

CSS_CORE = """
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,600;1,500&family=DM+Sans:wght@400;500&family=Dancing+Script:wght@500;600&display=swap');
:root{--blush:#F8D7E5;--rose:#EFA3BB;--cream:#FFF8F2;--burg:#7A2947;--red:#C44569;--ink:#4a1d31;
--serif:'Playfair Display','Georgia','Times New Roman',serif;--sans:'DM Sans',system-ui,-apple-system,'Segoe UI',sans-serif;
--script:'Dancing Script','Segoe Script','Brush Script MT',cursive;}
html,body,.stApp{overflow-x:hidden;color-scheme:light;}
.stApp,body{background:var(--cream);font-family:var(--sans);color:var(--ink);}
.script{font-family:var(--script);}

.hrt-layer{pointer-events:none;overflow:hidden;z-index:0;}
.hrt-layer.fixed{position:fixed;inset:0;}
.hrt-layer.local{position:absolute;inset:0;}
.hrt{position:absolute;bottom:-40px;left:var(--x);font-size:var(--s);color:var(--c);opacity:0;animation:floatup var(--d) linear var(--dl) infinite;}
@keyframes floatup{0%{transform:translateY(0) rotate(-8deg);opacity:0}10%{opacity:.5}90%{opacity:.35}100%{transform:translateY(var(--h,-110vh)) rotate(10deg);opacity:0}}
.spark{position:absolute;font-size:var(--s);color:#fff;text-shadow:0 0 10px #fff,0 0 18px var(--rose);opacity:.2;animation:twinkle 3.2s ease-in-out var(--dl) infinite;pointer-events:none;}
@keyframes twinkle{0%,100%{opacity:.15;transform:scale(.7)}50%{opacity:1;transform:scale(1.15)}}

.rise{animation:rise .9s ease both;}
@keyframes rise{from{opacity:0;transform:translateY(22px)}to{opacity:1;transform:none}}
@supports (animation-timeline:view()){.rise{animation:rise linear both;animation-timeline:view();animation-range:entry 0% entry 55%;}}
@keyframes glow{0%,100%{box-shadow:0 8px 22px rgba(196,69,105,.30)}50%{box-shadow:0 8px 34px rgba(196,69,105,.55)}}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.18)}}
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}

.wrap{max-width:1080px;margin:0 auto;padding:88px 24px 20px;}
.eyebrow{letter-spacing:.28em;text-transform:uppercase;font-size:.72rem;color:var(--red);text-align:center;font-weight:500;}
.h2{font-family:var(--serif);font-size:clamp(1.8rem,4.6vw,2.75rem);color:var(--burg);text-align:center;margin:.45rem 0 .3rem;line-height:1.2;}
.sub{text-align:center;color:#8a5468;max-width:560px;margin:0 auto 2.2rem;font-size:1.02rem;line-height:1.6;}
.flower{text-align:center;color:var(--rose);font-size:1.4rem;margin-bottom:.3rem;}

@BTN@{background:linear-gradient(135deg,#C44569,#d9667f)!important;color:#fff!important;border:0!important;border-radius:999px;padding:.8rem 2.2rem;
font-size:1rem;font-weight:500;font-family:var(--sans);letter-spacing:.02em;cursor:pointer;animation:glow 2.8s ease-in-out infinite;transition:transform .25s;}
@BTN@ p{color:#fff!important;margin:0;}
@BTN@:hover{transform:translateY(-2px) scale(1.04);}
@BTN@:disabled{opacity:.4;animation:none;cursor:not-allowed;filter:grayscale(.4);}

/* hero */
.S-hero{position:relative;overflow:hidden;gap:0;padding-bottom:72px;min-height:86vh;
background:
radial-gradient(circle at 8% 22%,rgba(255,255,255,.85) 0,rgba(255,255,255,0) 90px),
radial-gradient(circle at 90% 14%,rgba(239,163,187,.5) 0,rgba(239,163,187,0) 140px),
radial-gradient(circle at 80% 74%,rgba(255,255,255,.8) 0,rgba(255,255,255,0) 110px),
radial-gradient(circle at 18% 82%,rgba(239,163,187,.38) 0,rgba(239,163,187,0) 150px),
radial-gradient(circle at 52% 6%,rgba(255,214,170,.5) 0,rgba(255,214,170,0) 120px),
linear-gradient(165deg,#F8D7E5 0%,#FBE3EA 45%,#FFF8F2 100%);}
.hero-in{position:relative;max-width:900px;margin:0 auto;padding:96px 24px 18px;text-align:center;}
.hero-text{position:relative;z-index:1;}
.hero-h{font-family:var(--serif);font-size:clamp(2.5rem,8vw,5rem);line-height:1.08;color:var(--burg);margin:.7rem 0 .6rem;}
.hero-h em{color:var(--red);font-style:italic;}
.hero-script{font-family:var(--script);font-size:clamp(1.4rem,3.4vw,1.9rem);color:var(--red);margin:.3rem 0 .9rem;}
.hero-sub{max-width:520px;margin:0 auto;text-align:center;font-size:1.08rem;line-height:1.65;color:#6b3550;}
.gift{position:relative;width:112px;height:110px;margin:30px auto 18px;animation:bob 3.4s ease-in-out infinite;}
.gift .box{position:absolute;bottom:0;left:8px;right:8px;height:64px;background:linear-gradient(#e8708e,#c44569);border-radius:6px;box-shadow:0 14px 26px rgba(122,41,71,.28);}
.gift .lid{position:absolute;bottom:62px;left:0;right:0;height:26px;background:#d65a7c;border-radius:7px;}
.gift .box::after,.gift .lid::after{content:"";position:absolute;left:50%;width:16px;margin-left:-8px;top:0;bottom:0;background:var(--cream);}
.gift .bow{position:absolute;bottom:86px;left:50%;width:0;height:0;}
.gift .bow i{position:absolute;bottom:-6px;width:32px;height:22px;border:6px solid var(--cream);border-radius:60% 40% 60% 40%;}
.gift .bow i:first-child{right:-2px;transform:rotate(-24deg);}
.gift .bow i:last-child{left:-2px;transform:rotate(24deg) scaleX(-1);}
.gift .burst span{position:absolute;bottom:56px;left:50%;font-size:1.6rem;opacity:0;pointer-events:none;}
.gift.open::before{content:"";position:absolute;left:-46px;right:-46px;top:-6px;height:90px;background:radial-gradient(ellipse at 50% 100%,rgba(255,236,200,.95),rgba(255,236,200,0) 70%);animation:rise .8s ease both;}
.gift.open .box::before{content:"";position:absolute;top:0;left:0;right:0;height:10px;background:#8c2c4a;border-radius:6px 6px 0 0;}
.gift.open .lid{animation:lidup .8s cubic-bezier(.3,1.4,.5,1) forwards;}
.gift.open .bow{animation:bowup .8s cubic-bezier(.3,1.4,.5,1) forwards;}
.gift.open .burst span{animation:popout 2.6s ease-out forwards;animation-delay:calc(var(--i)*.14s + .3s);}
@keyframes lidup{to{transform:translate(-18px,-52px) rotate(-22deg)}}
@keyframes bowup{to{transform:translate(-18px,-52px) rotate(-22deg)}}
@keyframes popout{0%{opacity:0;transform:translate(-50%,0) scale(.4)}25%{opacity:1}100%{opacity:1;transform:translate(calc(-50% + var(--dx)),-118px) scale(1)}}
.surprise{position:relative;z-index:1;max-width:620px;margin:34px auto 0;padding:30px 30px 26px;text-align:center;background:rgba(255,255,255,.72);
border:1px solid rgba(239,163,187,.6);border-radius:22px;box-shadow:0 18px 44px rgba(122,41,71,.14);animation:rise .9s ease both;}
.surprise p{font-family:var(--serif);font-style:italic;font-size:1.2rem;line-height:1.7;color:var(--burg);margin:0 0 .6rem;}
.surprise .more{font-size:.78rem;letter-spacing:.2em;text-transform:uppercase;color:var(--red);animation:bob 2s ease-in-out infinite;}

/* gallery */
.feat-wrap{max-width:1080px;margin:10px auto 0;padding:0 24px;}
.feat-tag{text-align:center;font-family:var(--script);font-size:1.5rem;color:var(--red);margin-bottom:10px;}
.feat{max-width:520px;margin:0 auto;}
.feat .pol{box-shadow:0 0 0 8px rgba(248,215,229,.5),0 24px 60px rgba(196,69,105,.25);}
.scrap{max-width:1080px;margin:36px auto 0;padding:10px 28px 0;column-width:250px;column-gap:30px;}
.pol{position:relative;background:#fff;padding:12px 12px 14px;border-radius:10px;box-shadow:0 10px 28px rgba(122,41,71,.16);
transform:rotate(var(--rot,0deg));margin:0 0 32px;break-inside:avoid;transition:transform .35s ease,box-shadow .35s ease;}
.pol:hover{transform:rotate(0deg) translateY(-6px) scale(1.02);box-shadow:0 20px 40px rgba(122,41,71,.22);}
.pol .tape{position:absolute;top:-12px;left:50%;width:86px;height:24px;margin-left:-43px;background:rgba(239,163,187,.55);transform:rotate(-3deg);}
.pol img{width:100%;height:auto;display:block;border-radius:6px;}
.pol figcaption{font-family:var(--script);font-size:1.35rem;text-align:center;color:var(--burg);padding-top:10px;line-height:1.25;}
.ph{border:2px dashed var(--rose);border-radius:6px;background:linear-gradient(145deg,#FDE9F0,#FFF8F2);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:18px;color:#a8546f;}
.ph-a{aspect-ratio:4/5}.ph-b{aspect-ratio:1/1}.ph-c{aspect-ratio:4/3}
.ph-ico{font-size:2.3rem;animation:pulse 3s ease-in-out infinite;}
.ph-t{font-size:.9rem;margin-top:.5rem;line-height:1.4;}
.ph-s{font-size:.7rem;letter-spacing:.18em;text-transform:uppercase;margin-top:.5rem;opacity:.7;}

/* letter */
.letter{position:relative;max-width:720px;margin:36px auto 0;padding:48px 40px 40px 80px;background-color:#FFFDF9;
background-image:repeating-linear-gradient(transparent 0 33px,rgba(239,163,187,.25) 33px 34px);border-radius:6px;
box-shadow:0 22px 55px rgba(122,41,71,.16),0 0 0 1px rgba(239,163,187,.35);transform:rotate(-.4deg);}
.letter::before{content:"";position:absolute;top:0;bottom:0;left:56px;width:1px;background:rgba(196,69,105,.3);}
.letter p{font-family:var(--serif);font-size:1.05rem;line-height:34px;margin:0 0 34px;color:var(--ink);}
.letter .greet{font-family:var(--script);font-size:1.9rem;color:var(--red);line-height:34px;margin-bottom:34px;}
.letter .closing{font-family:var(--script);font-size:1.6rem;color:var(--burg);margin:0;line-height:38px;}
.letter .sig{font-size:1.9rem;color:var(--red);}
.lh{position:absolute;color:var(--rose);animation:pulse 3.4s ease-in-out infinite;}
.lh.a{top:10px;left:14px;font-size:1.3rem}.lh.b{top:12px;right:16px;font-size:1rem;animation-delay:.6s}
.lh.c{bottom:12px;left:20px;font-size:1rem;animation-delay:1.2s}.lh.d{bottom:10px;right:14px;font-size:1.4rem;animation-delay:1.8s}

/* quotes */
.qgrid{max-width:1080px;margin:0 auto;padding:10px 24px 0;display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:22px;}
.qcard{padding:28px 26px;border-radius:20px;font-family:var(--serif);font-style:italic;font-size:1.12rem;line-height:1.65;transition:transform .3s,box-shadow .3s;}
.qcard:hover{transform:translateY(-6px);box-shadow:0 18px 38px rgba(122,41,71,.18);}
.qcard .qh{display:block;font-style:normal;font-size:1.2rem;margin-bottom:.7rem;animation:pulse 3.2s ease-in-out infinite;}
.q0{background:linear-gradient(145deg,#F8D7E5,#fbe6ee);color:var(--burg)}
.q1{background:#fff;border:1px solid var(--blush);color:var(--ink)}
.q2{background:linear-gradient(145deg,#EFA3BB,#f3b9cb);color:#4d1630}
.q3{background:linear-gradient(145deg,#7A2947,#963a5b);color:#FFF8F2}
.q4{background:#FFF1EA;border:1px dashed var(--rose);color:var(--burg)}
.q5{background:linear-gradient(145deg,#fff,#FBE3EA);color:var(--ink)}
.q0 .qh,.q1 .qh,.q4 .qh,.q5 .qh{color:var(--red)}.q2 .qh{color:#fff}.q3 .qh{color:var(--rose)}

/* cake */
.S-wish{gap:0;padding-bottom:90px;background:linear-gradient(180deg,#FFF8F2 0%,#FCE6EE 100%);}
.cake{position:relative;width:250px;height:262px;margin:26px auto 78px;}
.tier{position:absolute;left:50%;transform:translateX(-50%);border-radius:14px 14px 10px 10px;box-shadow:0 8px 18px rgba(122,41,71,.18);}
.tier::before{content:"";position:absolute;left:0;right:0;top:0;height:22px;border-radius:inherit;background:radial-gradient(circle at 12px 0,#fff 0 11px,transparent 12px) 0 0/24px 22px repeat-x;}
.t1{bottom:0;width:240px;height:72px;background:linear-gradient(#f6b8cb,#ef9db7)}
.t2{bottom:72px;width:180px;height:62px;background:linear-gradient(#fff,#fde0ea)}
.t3{bottom:134px;width:120px;height:52px;background:linear-gradient(#e8708e,#c44569)}
.plate{position:absolute;bottom:-12px;left:50%;transform:translateX(-50%);width:292px;height:16px;border-radius:50%;background:#fff;box-shadow:0 6px 14px rgba(122,41,71,.2);}
.candle{position:absolute;bottom:186px;width:9px;height:36px;border-radius:3px;background:repeating-linear-gradient(135deg,#fff 0 6px,#EFA3BB 6px 12px);}
.candle::before{content:"";position:absolute;top:-3px;left:50%;width:2px;height:5px;margin-left:-1px;background:#5a3a3a;}
.flame{position:absolute;top:-20px;left:50%;width:12px;height:19px;margin-left:-6px;border-radius:50% 50% 50% 50%/62% 62% 38% 38%;
background:radial-gradient(ellipse at 50% 70%,#fff5b8,#ffb347 62%,transparent 74%);box-shadow:0 0 14px 4px rgba(255,190,90,.55);transform-origin:50% 100%;animation:flick 1.3s ease-in-out infinite alternate;}
@keyframes flick{0%{transform:scale(1,1) rotate(-3deg)}50%{transform:scale(.9,1.12) rotate(2deg)}100%{transform:scale(1.05,.94) rotate(-2deg)}}
.cake.out .flame{display:none;}
.cake.out .candle::after{content:"";position:absolute;left:50%;top:-8px;width:8px;height:8px;margin-left:-4px;border-radius:50%;background:rgba(120,100,110,.5);filter:blur(3px);animation:smoke 2.2s ease-out 3;opacity:0;}
@keyframes smoke{0%{transform:translateY(0) scale(.6);opacity:.7}100%{transform:translateY(-48px) scale(2.3);opacity:0}}
.cake-note{text-align:center;font-family:var(--script);font-size:1.6rem;color:var(--red);min-height:2.2rem;margin-top:-34px;padding:0 10px;}
.cut-gap{position:absolute;left:calc(50% + 14px);bottom:0;width:30px;height:186px;z-index:2;display:none;border-radius:4px 4px 0 0;
background:repeating-linear-gradient(#fff3e6 0 18px,#f6b8cb 18px 24px);box-shadow:inset 6px 0 8px rgba(122,41,71,.18),inset -4px 0 6px rgba(122,41,71,.12);}
.knife{position:absolute;left:calc(50% + 6px);top:-6px;font-size:2rem;opacity:0;z-index:4;pointer-events:none;}
.slice{position:absolute;left:calc(50% - 28px);bottom:-70px;width:56px;height:54px;z-index:3;display:none;}
.slice i{display:block;}
.slice .s1{height:16px;background:#C44569;border-radius:8px 8px 0 0;}
.slice .s2{height:18px;background:linear-gradient(#fff,#fde0ea);}
.slice .s3{height:20px;background:#ef9db7;border-radius:0 0 4px 4px;}
.slice .sp{position:absolute;left:-12px;right:-12px;bottom:-7px;height:10px;border-radius:50%;background:#fff;box-shadow:0 4px 8px rgba(122,41,71,.2);z-index:-1;}
.cake.cut .cut-gap{display:block;animation:gapopen .6s .9s both;}
.cake.cut .knife{animation:knife 1.7s ease forwards;}
.cake.cut .slice{display:block;animation:slicein .6s 1.3s both;}
@keyframes gapopen{from{width:0;opacity:0}to{width:30px;opacity:1}}
@keyframes knife{0%{opacity:0;transform:translateY(-24px) rotate(-30deg)}25%{opacity:1;transform:translateY(0) rotate(-12deg)}75%{opacity:1;transform:translateY(150px) rotate(-6deg)}100%{opacity:0;transform:translateY(150px) rotate(-6deg)}}
@keyframes slicein{from{opacity:0;transform:translateY(-60px)}to{opacity:1;transform:none}}
.wish-card{max-width:660px;margin:30px auto 0;padding:30px 30px 26px;text-align:center;background:rgba(255,255,255,.8);border:1px solid rgba(239,163,187,.6);
border-radius:22px;box-shadow:0 18px 44px rgba(122,41,71,.14);animation:rise .9s ease both;}
.wish-card p{font-family:var(--serif);font-style:italic;font-size:1.15rem;line-height:1.7;color:var(--burg);margin:0 0 .9rem;}
.wish-card .big{font-family:var(--script);font-size:1.7rem;color:var(--red);font-style:normal;line-height:1.4;margin:0;}

/* timeline */
.tl{position:relative;max-width:920px;margin:0 auto;padding:10px 24px 0;}
.tl::before{content:"";position:absolute;left:50%;top:0;bottom:30px;width:2px;transform:translateX(-50%);background:linear-gradient(var(--rose),var(--blush));}
.tl-item{position:relative;width:50%;box-sizing:border-box;padding:0 46px 40px 0;}
.tl-item:nth-child(even){margin-left:50%;padding:0 0 40px 46px;}
.tl-dot{position:absolute;top:10px;right:-14px;width:28px;height:28px;border-radius:50%;background:#fff;border:2px solid var(--rose);color:var(--red);
display:flex;align-items:center;justify-content:center;font-size:.8rem;animation:pulse 3s ease-in-out infinite;}
.tl-item:nth-child(even) .tl-dot{right:auto;left:-14px;}
.tl-card{background:rgba(255,255,255,.8);border:1px solid rgba(239,163,187,.55);border-radius:18px;padding:20px 22px;box-shadow:0 10px 26px rgba(122,41,71,.09);transition:transform .3s;}
.tl-card:hover{transform:translateY(-4px);}
.tl-card img{width:100%;height:auto;border-radius:12px;margin-bottom:14px;display:block;}
.tl-t{font-family:var(--serif);font-size:1.25rem;color:var(--burg);margin-bottom:.3rem;}
.tl-p{margin:0;color:#6b3550;line-height:1.6;font-size:.98rem;}
@media (max-width:720px){
.tl::before{left:38px}.tl-item,.tl-item:nth-child(even){width:100%;margin-left:0;padding:0 0 30px 58px;}
.tl-dot,.tl-item:nth-child(even) .tl-dot{left:24px;right:auto;}
.letter{padding:38px 22px 34px 46px;}.letter::before{left:30px;}
.wrap{padding-top:64px;}}

/* reasons */
.band{background:linear-gradient(180deg,#FBE6EE,#F8D7E5);margin-top:70px;padding-bottom:90px;}
.rgrid{max-width:1080px;margin:0 auto;padding:0 24px;display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:20px;}
.rcard{background:rgba(255,255,255,.7);border:1px solid rgba(255,255,255,.9);border-radius:20px;padding:24px 22px;text-align:center;box-shadow:0 8px 22px rgba(122,41,71,.08);transition:transform .3s,box-shadow .3s,background .3s;}
.rcard:hover{transform:translateY(-6px);background:#fff;box-shadow:0 18px 36px rgba(122,41,71,.16);}
.rcard .ri{font-size:1.7rem;display:block;margin-bottom:.5rem;animation:pulse 3.4s ease-in-out infinite;}
.rcard .rt{font-family:var(--serif);color:var(--burg);font-size:1.12rem;margin-bottom:.3rem;}
.rcard .rp{color:#6b3550;font-size:.93rem;line-height:1.55;margin:0;}

/* finale */
.S-finale{position:relative;overflow:hidden;gap:0;padding-bottom:64px;color:var(--cream);
background:radial-gradient(circle at 50% 0%,rgba(196,69,105,.45),rgba(196,69,105,0) 60%),linear-gradient(180deg,#6a2340,#4a1730);}
.fin-in{position:relative;max-width:700px;margin:0 auto;padding:96px 24px 10px;text-align:center;}
.fin-in .fz{position:relative;z-index:1;}
.fin-h{font-family:var(--serif);font-size:clamp(1.9rem,5.2vw,3.2rem);line-height:1.2;color:#FFF8F2;margin:.5rem 0 0;}
.arch{position:relative;width:min(300px,78vw);margin:38px auto 34px;padding:10px;border-radius:200px 200px 22px 22px;background:linear-gradient(145deg,rgba(248,215,229,.95),rgba(239,163,187,.65));
box-shadow:0 0 0 7px rgba(248,215,229,.14),0 0 60px rgba(239,163,187,.45);animation:glowframe 4.5s ease-in-out infinite;}
.arch::before{content:"❤";position:absolute;top:-20px;left:50%;margin-left:-14px;font-size:1.7rem;color:#F8D7E5;text-shadow:0 0 14px #EFA3BB;animation:pulse 2.6s ease-in-out infinite;}
.arch .in{border-radius:190px 190px 14px 14px;overflow:hidden;background:#FFF8F2;}
.arch img{width:100%;aspect-ratio:3/4;object-fit:cover;display:block;}
.arch .ph{border:0;border-radius:0;aspect-ratio:3/4;}
@keyframes glowframe{0%,100%{box-shadow:0 0 0 7px rgba(248,215,229,.12),0 0 40px rgba(239,163,187,.35)}50%{box-shadow:0 0 0 9px rgba(248,215,229,.2),0 0 76px rgba(239,163,187,.6)}}
.fin-p{font-size:1.08rem;line-height:1.8;color:#f5dfe7;margin:0 0 1.1rem;}
.hug{position:relative;z-index:1;max-width:600px;margin:30px auto 0;padding:26px 28px;text-align:center;background:rgba(255,248,242,.08);border:1px solid rgba(248,215,229,.35);border-radius:20px;animation:rise .9s ease both;}
.hug p{font-family:var(--serif);font-style:italic;font-size:1.15rem;line-height:1.7;color:#FFF8F2;margin:0;}
.S-finale @BTN@{background:#FFF8F2!important;box-shadow:0 0 28px rgba(248,215,229,.4);}
.S-finale @BTN@,.S-finale @BTN@ p{color:#7A2947!important;}
.foot{position:relative;z-index:1;text-align:center;font-family:var(--script);font-size:1.7rem;color:var(--blush);margin-top:54px;}

/* confetti */
.cf-layer{position:fixed;inset:0;pointer-events:none;z-index:9999;overflow:hidden;}
.cf{position:absolute;top:-24px;width:var(--s);height:calc(var(--s)*.6);background:var(--c);opacity:0;border-radius:2px;animation:cffall var(--d) ease-in var(--dl) forwards;}
.cf.h{background:none;width:auto;height:auto;font-size:var(--s);color:var(--c);}
.cf.h::before{content:"❤";}
@keyframes cffall{0%{opacity:1;transform:translate(0,0) rotate(0)}85%{opacity:1}100%{opacity:0;transform:translate(var(--dx),105vh) rotate(var(--r))}}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important;}}
"""

CSS_APP = """
header[data-testid="stHeader"],#MainMenu,footer,[data-testid="stToolbar"],[data-testid="stDecoration"],[data-testid="stStatusWidget"]{display:none!important;}
[data-testid="stMainBlockContainer"],.block-container{max-width:100%!important;padding:0!important;position:relative;z-index:1;}
[data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"]{gap:0;}
div[data-testid="stButton"]{display:flex;justify-content:center;}
.st-key-wish [data-testid="stHorizontalBlock"]{max-width:800px;margin:0 auto;padding:0 16px;gap:.8rem;}
"""


def build_css() -> str:
    return (CSS_CORE.replace(".S-", ".st-key-")
            .replace("@BTN@", 'div[data-testid="stButton"] button') + CSS_APP)


# =============================================================================
# Page pieces (HTML builders)
# =============================================================================

BURST = [("💖", -46), ("🎈", -18), ("✨", 6), ("🎉", 30), ("💌", 52)]


def hero_main_html(cfg: dict, opened: bool) -> str:
    gift_cls = "gift open" if opened else "gift"
    burst = "".join(f'<span style="--dx:{dx}px;--i:{i}">{e}</span>' for i, (e, dx) in enumerate(BURST))
    return f"""
    <div class="hero-in">
    {hearts_html(14, 3, rise="-760px")}
    {sparks_html(9, 11)}
    <div class="hero-text">
    <div class="eyebrow">{esc(HERO_EYEBROW)}</div>
    <div class="hero-h" role="heading" aria-level="1">Happy Birthday,<br><em>{esc(cfg["her"])}</em> ❤️</div>
    <div class="hero-script">{esc(HERO_SCRIPT)}</div>
    <div class="hero-sub">{esc(HERO_SUBTITLE)}</div>
    <div class="{gift_cls}" id="gift"><div class="burst">{burst}</div><div class="bow"><i></i><i></i></div><div class="lid"></div><div class="box"></div></div>
    </div>
    </div>
    """


def surprise_html(cfg: dict) -> str:
    return f'<div class="surprise"><p>{esc(cfg["surprise"])}</p><div class="more">Keep scrolling ↓</div></div>'


def gallery_head_html() -> str:
    return f"""
    <div class="wrap">
    <div class="flower">✿</div>
    <div class="eyebrow">A place for our story</div>
    <div class="h2">{esc(GALLERY_TITLE)}</div>
    <div class="sub">{esc(GALLERY_SUBTITLE)}</div>
    </div>
    """


def polaroid(photo, caption: str, k: int, big: bool = False, ratio: str | None = None) -> str:
    rot = 0 if big else [-2.4, 1.8, -1.1, 2.6, -1.9, 1.2, -2.8, 2.1][k % 8]
    if photo:
        body = f'<img src="{photo["uri"]}" alt="{esc(caption)}" loading="lazy">'
    else:
        cls = ratio or ["ph-a", "ph-b", "ph-c"][k % 3]
        icon = "📷" if k % 2 else "♡"
        body = (f'<div class="ph {cls}"><div class="ph-ico">{icon}</div>'
                f'<div class="ph-t">Our favourite memory belongs here.</div>'
                f'<div class="ph-s">Reserved for your photograph</div></div>')
    return (f'<figure class="pol" style="--rot:{rot}deg"><div class="tape"></div>{body}'
            f'<figcaption>{esc(caption)}</figcaption></figure>')


def gallery_body_html(feat_photo, items) -> str:
    featured = f"""
    <div class="feat-wrap rise">
    <div class="feat-tag">✨ Our favourite ✨</div>
    <div class="feat">{polaroid(feat_photo, FEATURED_CAPTION, 0, big=True, ratio="ph-c")}</div>
    </div>
    """
    tiles = [polaroid(photo, cap, k) for k, (photo, cap) in enumerate(items)]
    if not tiles:  # nothing listed at all -> show lovely placeholders
        tiles = [polaroid(None, DEFAULT_CAPTIONS[k % len(DEFAULT_CAPTIONS)], k) for k in range(6)]
    return featured + f'<div class="scrap rise">{"".join(tiles)}</div>'


def letter_html(cfg: dict) -> str:
    corners = '<span class="lh a">♡</span><span class="lh b">❤</span><span class="lh c">❤</span><span class="lh d">♡</span>'
    return f"""
    <div class="wrap">
    <div class="eyebrow">Handwritten with love</div>
    <div class="h2">A Little Letter for My Favourite Human</div>
    <div class="letter rise">
    {corners}
    <p class="greet">{esc(LETTER_GREETING)}</p>
    {paragraphs(cfg["letter"])}
    <p class="closing">{esc(LETTER_CLOSING)}<br><span class="sig">{esc(cfg["me"])}</span></p>
    </div>
    </div>
    """


def quotes_html() -> str:
    cards = "".join(f'<div class="qcard q{i % 6} rise"><span class="qh">❤</span>{esc(q)}</div>'
                    for i, q in enumerate(QUOTES))
    return f"""
    <div class="wrap">
    <div class="eyebrow">Little reminders</div>
    <div class="h2">A Few Things I Hope You Never Forget ❤️</div>
    <div class="sub">Say them out loud when you need to.</div>
    </div>
    <div class="qgrid">{cards}</div>
    """


def wish_head_html(cake_cls: str, note: str) -> str:
    return f"""
    <div class="wrap">
    <div class="eyebrow">Close your eyes</div>
    <div class="h2">Make a Birthday Wish ✨</div>
    <div class="{cake_cls}" id="cake">
    <div class="candle" style="left:calc(50% - 30px)"><div class="flame"></div></div>
    <div class="candle" style="left:calc(50% - 4px)"><div class="flame" style="animation-delay:.3s"></div></div>
    <div class="candle" style="left:calc(50% + 22px)"><div class="flame" style="animation-delay:.6s"></div></div>
    <div class="tier t3"></div><div class="tier t2"></div><div class="tier t1"></div><div class="plate"></div>
    <div class="cut-gap"></div>
    <div class="slice"><i class="s1"></i><i class="s2"></i><i class="s3"></i><span class="sp"></span></div>
    <div class="knife">🔪</div>
    </div>
    <div class="cake-note" id="note">{esc(note)}</div>
    </div>
    """


def wish_card_html() -> str:
    return f'<div class="wish-card"><p>{esc(WISH_TEXT)}</p><p class="big">{esc(WISH_CELEBRATION)}</p></div>'


def timeline_html() -> str:
    items = []
    for e in TIMELINE:
        photo = get_photo(e.get("photo"))
        img = f'<img src="{photo["uri"]}" alt="{esc(e["title"])}" loading="lazy">' if photo else ""
        items.append(
            f'<div class="tl-item rise"><span class="tl-dot">❤</span><div class="tl-card">{img}'
            f'<div class="tl-t">{esc(e["title"])}</div><p class="tl-p">{esc(e["text"])}</p></div></div>'
        )
    return f"""
    <div class="wrap">
    <div class="eyebrow">Our story so far</div>
    <div class="h2">Little Moments, Big Feelings</div>
    <div class="sub">A few chapters, and so many more to write.</div>
    </div>
    <div class="tl">{"".join(items)}</div>
    """


def reasons_html() -> str:
    cards = "".join(
        f'<div class="rcard rise"><span class="ri">{esc(i)}</span><div class="rt">{esc(t)}</div><p class="rp">{esc(p)}</p></div>'
        for i, t, p in REASONS
    )
    return f"""
    <div class="band">
    <div class="wrap">
    <div class="eyebrow">The little things, the big things</div>
    <div class="h2">A Few of My Favourite Things About You</div>
    <div class="sub">Only eight, because I'd never finish the list.</div>
    </div>
    <div class="rgrid">{cards}</div>
    </div>
    """


def finale_main_html(photo) -> str:
    if photo:
        inner = f'<img src="{photo["uri"]}" alt="Our favourite picture">'
    else:
        inner = ('<div class="ph"><div class="ph-ico">❤</div><div class="ph-t">Our favourite picture goes here.</div>'
                 '<div class="ph-s">Reserved for your photograph</div></div>')
    paras = "".join(f'<p class="fin-p">{esc(p)}</p>' for p in FINAL_PARAGRAPHS)
    return f"""
    <div class="fin-in">
    {hearts_html(18, 21, rise="-1000px")}
    <div class="fz">
    <div class="eyebrow" style="color:#EFA3BB">One last thing</div>
    <div class="fin-h">{esc(FINAL_TITLE)}</div>
    <div class="arch"><div class="in">{inner}</div></div>
    {paras}
    </div>
    </div>
    """


def hug_html() -> str:
    return f'<div class="hug"><p>{esc(HUG_MESSAGE)}</p></div>'


def foot_html() -> str:
    return f'<div class="foot">{esc(FOOTER_LINE)}</div>'


# =============================================================================
# Streamlit app
# =============================================================================


def init_state() -> None:
    for k, v in {"opened": False, "wish_n": 0, "hug_n": 0, "candles_out": False,
                 "cake_cut": False, "cake_last": "", "cake_fx": 0}.items():
        st.session_state.setdefault(k, v)


def section_hero(cfg):
    ss = st.session_state

    def toggle():
        ss.opened = not ss.opened

    with st.container(key="hero"):
        render(hero_main_html(cfg, ss.opened))
        st.button("Fold it back up 💌" if ss.opened else "Open Your Surprise 💌", key="open_btn", on_click=toggle)
        if ss.opened:
            render(surprise_html(cfg))


def section_wish():
    ss = st.session_state

    def blow():
        ss.candles_out, ss.cake_last = True, "blow"
        ss.cake_fx += 1

    def cut():
        ss.cake_cut, ss.cake_last = True, "cut"
        ss.cake_fx += 1

    def relight():
        ss.candles_out = ss.cake_cut = False
        ss.cake_last = ""

    def send_love():
        ss.wish_n += 1

    out, is_cut = ss.candles_out, ss.cake_cut
    cls = "cake" + (" out" if out else "") + (" cut" if is_cut else "")
    note = NOTE_CUT if is_cut else (NOTE_OUT if out else NOTE_IDLE)

    with st.container(key="wish"):
        render(wish_head_html(cls, note))
        _, c1, c2, c3, _ = st.columns([1, 2, 2, 2, 1])
        c1.button("Blow out the candles 🌬️", key="blow_btn", on_click=blow, disabled=out)
        c2.button("Cut the cake 🔪", key="cut_btn", on_click=cut, disabled=(not out) or is_cut)
        c3.button("Relight 🕯️", key="relight_btn", on_click=relight, disabled=not out)
        if ss.cake_last in ("blow", "cut"):
            render(confetti_html(seed=5000 + ss.cake_fx, n=50))
        render('<div style="height:28px"></div>')
        st.button("Send You All My Love 💗", key="wish_btn", on_click=send_love)
        if ss.wish_n > 0:
            render(confetti_html(seed=ss.wish_n))
            render(wish_card_html())


def section_finale(final_photo):
    ss = st.session_state

    def hug():
        ss.hug_n += 1

    with st.container(key="finale"):
        render(finale_main_html(final_photo))
        st.button("One More Hug? 🤗", key="hug_btn", on_click=hug)
        if ss.hug_n > 0:
            render(confetti_html(seed=1000 + ss.hug_n, n=45))
            render(hug_html())
        render(foot_html())


def main():
    init_state()
    render(f"<style>{build_css()}</style>")
    cfg = {"her": HER_NAME, "me": MY_NAME, "surprise": SURPRISE_MESSAGE, "letter": LETTER_PARAGRAPHS}
    render(hearts_html(16, 5))
    section_hero(cfg)
    render(gallery_head_html())
    render(gallery_body_html(get_photo(FEATURED_IMAGE), gallery_items()))
    render(letter_html(cfg))
    render(quotes_html())
    section_wish()
    render(timeline_html())
    render(reasons_html())
    section_finale(get_photo(FINAL_IMAGE))


if __name__ == "__main__":
    main()