#!/usr/bin/env python3
"""WCAG contrast of variant A's watch-face text: the disc is the page colour at 82 % over the orb,
so the worst cases are the disc over the darkest and the lightest orb pixel, per mode.

Usage: python3 -I docs/homepage/preview-clock/contrast.py
"""


def hex_rgb(value):
    value = value.lstrip('#')
    return [int(value[i:i + 2], 16) for i in (0, 2, 4)]


def luminance(rgb):
    def channel(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def over(top, alpha, below):
    return [round(alpha * t + (1 - alpha) * b) for t, b in zip(top, below)]


NAVY, OFF_WHITE, WHITE = hex_rgb('#191f38'), hex_rgb('#fffbf6'), hex_rgb('#ffffff')
# Day: navy text on an off-white disc; Night: off-white text on a navy disc (kc-tokens.css)
for mode, ink, page in (('day', NAVY, OFF_WHITE), ('night', OFF_WHITE, NAVY)):
    for orb_name, orb in (('darkest orb (#191f38)', NAVY), ('lightest orb (#ffffff)', WHITE)):
        disc = over(page, 0.82, orb)
        print(f'{mode:5} disc over {orb_name:22}: {contrast(ink, disc):5.2f}:1')
