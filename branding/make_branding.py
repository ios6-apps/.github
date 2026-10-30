"""Draws the ios6-apps organization logo (logo.png, 1024 px) and a 1280x640 social preview per app (social/<repo>.png).

    python3 make_branding.py [directory holding the app repositories]

Needs Pillow and the macOS Helvetica font. The app icons are read from <repo>/docs/icon.png.
"""
import os, random, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

FONT = "/System/Library/Fonts/Helvetica.ttc"
def font(size, bold=True): return ImageFont.truetype(FONT, size, index=1 if bold else 0)

def vgrad(w, h, top, bot):
    col = Image.new("RGB", (1, h))
    for y in range(h):
        t = y / max(1, h - 1)
        col.putpixel((0, y), tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    return col.resize((w, h))

def linen(w, h, seed=7):
    """Fine woven texture, the iOS 6 backdrop."""
    rnd = random.Random(seed)
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for x in range(0, w, 4):
        d.line([(x, 0), (x, h)], fill=(255, 255, 255, rnd.choice((6, 9, 12))), width=2)
    for y in range(0, h, 4):
        d.line([(0, y), (w, y)], fill=(0, 0, 0, rnd.choice((8, 12, 16))), width=2)
    return lay

def backdrop(w, h):
    bg = vgrad(w, h, (96, 128, 166), (30, 48, 76)).convert("RGBA")
    bg = Image.alpha_composite(bg, linen(w, h))
    glow = Image.new("L", (w, h), 0)
    ImageDraw.Draw(glow).ellipse([w * 0.1, -h * 0.55, w * 0.9, h * 0.45], fill=70)
    glow = glow.filter(ImageFilter.GaussianBlur(w * 0.08))
    bg.paste((255, 255, 255), (0, 0), glow)
    return bg

def shadowed(base, layer_mask, blur, dy, alpha):
    sh = layer_mask.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * alpha))
    sh = ImageChops.offset(sh, 0, dy)
    base.paste((0, 0, 0), (0, 0), sh)

def rounded_mask(size, r):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=r, fill=255)
    return m

def phone(S):
    """An iPhone 5 seen from the front, with a big 6 on the screen. Returns an RGBA image of S x S."""
    s = 2                                    # supersampling
    W = S * s
    im = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    pw, ph = int(W * 0.40), int(W * 0.80)    # 5s proportions are close to 1 : 2
    x0, y0 = (W - pw) // 2, (W - ph) // 2
    body = [x0, y0, x0 + pw, y0 + ph]
    mask = Image.new("L", (W, W), 0)
    ImageDraw.Draw(mask).rounded_rectangle(body, radius=int(pw * 0.17), fill=255)
    shadowed(im, mask, W * 0.025, int(W * 0.02), 0.55)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(body, radius=int(pw * 0.17), fill=(190, 196, 206))                       # aluminium rim
    r = int(pw * 0.012)
    d.rounded_rectangle([body[0] + r, body[1] + r, body[2] - r, body[3] - r], radius=int(pw * 0.16), fill=(24, 25, 29))
    # screen
    mx, top, bot = int(pw * 0.075), int(ph * 0.115), int(ph * 0.135)
    scr = [x0 + mx, y0 + top, x0 + pw - mx, y0 + ph - bot]
    sw, sh_ = scr[2] - scr[0], scr[3] - scr[1]
    screen = vgrad(sw, sh_, (86, 138, 206), (22, 58, 120)).convert("RGBA")
    screen = Image.alpha_composite(screen, linen(sw, sh_))
    # the 6
    g = ImageDraw.Draw(screen)
    f = font(int(sh_ * 0.78))
    bb = g.textbbox((0, 0), "6", font=f)
    tx, ty = (sw - (bb[2] - bb[0])) // 2 - bb[0], (sh_ - (bb[3] - bb[1])) // 2 - bb[1]
    tm = Image.new("L", (sw, sh_), 0)
    ImageDraw.Draw(tm).text((tx, ty), "6", font=f, fill=255)
    shadowed(screen, tm, sh_ * 0.012, int(sh_ * 0.018), 0.6)
    ImageDraw.Draw(screen).text((tx, ty), "6", font=f, fill=(255, 255, 255))
    # glossy sheen across the upper half
    gl = Image.new("RGBA", (sw, sh_), (0, 0, 0, 0))
    ImageDraw.Draw(gl).polygon([(0, 0), (sw, 0), (sw, int(sh_ * 0.22)), (0, int(sh_ * 0.50))], fill=(255, 255, 255, 40))
    screen = Image.alpha_composite(screen, gl)
    im.paste(screen, (scr[0], scr[1]), rounded_mask((sw, sh_), int(pw * 0.025)))
    d = ImageDraw.Draw(im)
    # speaker, camera, home button
    cx = x0 + pw // 2
    d.rounded_rectangle([cx - pw * 0.12, y0 + top * 0.5 - pw * 0.012, cx + pw * 0.12, y0 + top * 0.5 + pw * 0.012], radius=pw * 0.012, fill=(70, 72, 80))
    d.ellipse([cx - pw * 0.19 - pw * 0.014, y0 + top * 0.5 - pw * 0.014, cx - pw * 0.19 + pw * 0.014, y0 + top * 0.5 + pw * 0.014], fill=(48, 52, 70))
    hy = y0 + ph - bot * 0.5
    hr = pw * 0.085
    d.ellipse([cx - hr, hy - hr, cx + hr, hy + hr], fill=(60, 62, 70))
    d.ellipse([cx - hr + pw * 0.006, hy - hr + pw * 0.006, cx + hr - pw * 0.006, hy + hr - pw * 0.006], fill=(24, 25, 29))
    d.rounded_rectangle([cx - pw * 0.03, hy - pw * 0.03, cx + pw * 0.03, hy + pw * 0.03], radius=pw * 0.008, outline=(110, 112, 120), width=max(2, int(pw * 0.007)))
    return im.resize((S, S), Image.LANCZOS)

def logo(S=1024):
    bg = backdrop(S, S)
    ph = phone(S)
    bg = Image.alpha_composite(bg, ph)
    return bg.convert("RGB")

def social(name, tagline, icon_path, W=1280, H=640):
    bg = backdrop(W, H)
    ic = Image.open(icon_path).convert("RGBA").resize((384, 384), Image.LANCZOS)
    m = ic.split()[3]
    sh = Image.new("L", (W, H), 0); sh.paste(m, (110, 128))
    shadowed(bg, sh, 18, 14, 0.6)
    bg.alpha_composite(ic, (110, 128))
    d = ImageDraw.Draw(bg)
    x = 570
    fs = 104
    while d.textlength(name, font=font(fs)) > W - x - 70: fs -= 4
    d.text((x, 190), name, font=font(fs), fill=(255, 255, 255))
    f2 = font(38, bold=False)
    words, line, y = tagline.split(), "", 190 + fs + 34
    for w_ in words:
        t = (line + " " + w_).strip()
        if d.textlength(t, font=f2) > W - x - 70:
            d.text((x, y), line, font=f2, fill=(205, 218, 235)); y += 52; line = w_
        else: line = t
    d.text((x, y), line, font=f2, fill=(205, 218, 235))
    d.text((x, H - 96), "iOS 6  ·  open source  ·  ios6-apps", font=font(30, bold=False), fill=(150, 172, 200))
    return bg.convert("RGB")

APPS = {
    "ios6-hnreader": ("HN Reader", "Hacker News for iOS 6: reader view, comments and offline saved stories."),
    "ios6-redditreader": ("Reddit Reader", "Reddit for iOS 6 from the public feeds: pictures, GIFs and video."),
    "ios6-kodiremote": ("Kodi Remote", "Remote control for Kodi over JSON-RPC, with typing into text boxes."),
    "ios6-tumbler": ("Tumbler", "TOTP and HOTP authenticator for iOS 6 with QR scanning and a PIN lock."),
    "ios6-tvremote": ("TV Remote", "A wood-and-plastic remote for Android TV and Google TV."),
}

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "..", "..")
    logo().save(os.path.join(here, "logo.png"))
    os.makedirs(os.path.join(here, "social"), exist_ok=True)
    for repo, (name, tag) in APPS.items():
        icon = os.path.join(root, repo, "docs", "icon.png")
        social(name, tag, icon).save(os.path.join(here, "social", repo + ".png"))
    print("done")
