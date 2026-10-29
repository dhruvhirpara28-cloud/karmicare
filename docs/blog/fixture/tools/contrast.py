"""WCAG contrast of the blog's text and control colours in Day and Night, from assets/kc-tokens.css values.

usage: python3 -I contrast.py
Translucent colours are blended over the surface they sit on. Text needs 4.5:1 (3:1 at 24px or
19px bold and up); UI parts and focus rings need 3:1 (WCAG 1.4.3, 1.4.11).
"""


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def blend(fg, alpha, bg):
    return tuple(round(f * alpha + b * (1 - alpha)) for f, b in zip(fg, bg))


def lum(rgb):
    def ch(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


MODES = {
    "Day": dict(page="#fffbf6", accent="#f2f8ff", card="#ffffff", heading="#191f38", body=("#191f38", 0.76),
                hover="#7fb9ff", focus="#191f38", control=("#191f38", 0.76), btn_bg="#191f38", btn_fg="#fffbf6",
                btn_hover="#212a49", quote_rule="#7fb9ff"),
    "Night": dict(page="#191f38", accent="#2c3a60", card="#212a49", heading="#fffbf6", body=("#fffbf6", 0.68),
                  hover="#7fb9ff", focus="#fffbf6", control=("#fffbf6", 0.68), btn_bg="#fffbf6", btn_fg="#191f38",
                  btn_hover="#efece8", quote_rule="#7fb9ff"),
}

for mode, t in MODES.items():
    print(f"== {mode}")
    for sname in ("page", "accent", "card"):
        bg = hex2rgb(t[sname])
        body = blend(hex2rgb(t["body"][0]), t["body"][1], bg)
        ctrl = blend(hex2rgb(t["control"][0]), t["control"][1], bg)
        rows = [
            ("heading / title / links", hex2rgb(t["heading"]), 4.5),
            ("body, meta, captions (text-default-body)", body, 4.5),
            ("link hover (link-default-hover)", hex2rgb(t["hover"]), 4.5),
            ("focus ring (border-focus-strong)", hex2rgb(t["focus"]), 3.0),
            ("rail dots, pagination border (border-control)", ctrl, 3.0),
            ("quote rule (surface-accent, decorative)", hex2rgb(t["quote_rule"]), 0),
        ]
        for name, fg, need in rows:
            r = ratio(fg, bg)
            verdict = "decorative" if need == 0 else ("ok" if r >= need else f"BELOW {need}")
            print(f"  on {sname:6} {name:48} {r:5.2f}:1  {verdict}")
    print(f"  button label on button                                   {ratio(hex2rgb(t['btn_fg']), hex2rgb(t['btn_bg'])):5.2f}:1")
    print(f"  button label on hover                                    {ratio(hex2rgb(t['btn_fg']), hex2rgb(t['btn_hover'])):5.2f}:1")
    print(f"  button edge vs page                                      {ratio(hex2rgb(t['btn_bg']), hex2rgb(t['page'])):5.2f}:1")
