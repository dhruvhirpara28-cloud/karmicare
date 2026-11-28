"""Per variant and selected plan (Try once, 60-Day, Year): the promises under the CTA, the CTA, any text
line shown twice between the plans header and the promises (case-insensitive), and the ribbon's place
(its centre on the card's top border, horizontally between the title's end and the price's start).
Usage: python3 -I state_check.py <page-id> <port> <out.json> [variant ...]"""
import json
import subprocess
import sys
import time

PAGE, PORT, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
VARIANTS = sys.argv[4:] or ['on', 'full']
PROBE = r"""JSON.stringify((() => {
  const box = document.querySelector('.kc-buybox');
  const vis = (el) => el && el.checkVisibility();
  const promises = Array.from(box.querySelectorAll('.icon-with-text__item')).filter(vis).map((li) => li.innerText.trim());
  // Visible text lines from the plans header to the promises row, leaf blocks only
  const head = box.querySelector('.loop-purchase-options-label');
  const end = box.querySelector('.icon-with-text');
  const lines = [];
  const walker = document.createTreeWalker(box, NodeFilter.SHOW_TEXT);
  let started = false;
  while (walker.nextNode()) {
    const node = walker.currentNode;
    const el = node.parentElement;
    if (!started && head.contains(el)) started = true;
    // Stop after the promises row: what follows ("What you'll feel" …) is not the buybox
    if (!end.contains(el) && (end.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING)) break;
    if (!started || !vis(el) || !node.textContent.trim()) continue;
    if (el.closest('.info-tip-popover, .loop-hidden, script, style, option, select')) continue;
    lines.push(node.textContent.replace(/\s+/g, ' ').trim());
    if (end.contains(el) && el === end.querySelector('.icon-with-text__item:last-child .inline-richtext')) break;
  }
  const counts = {};
  lines.filter((l) => l.length > 6 && !/^[€\d\s.,/+·-]+$/.test(l)).forEach((l) => { const k = l.toLowerCase(); counts[k] = (counts[k] || 0) + 1; });
  const twice = Object.keys(counts).filter((k) => counts[k] > 1);
  let ribbon = null;
  const band = box.querySelector('.kc-plan-badge .kc-testimonial-button');
  if (vis(band)) {
    const card = band.closest('.loop-subscription-group');
    const b = band.getBoundingClientRect(), c = card.getBoundingClientRect();
    const title = card.querySelector('.loop-subscription-group-label');
    const range = document.createRange(); range.selectNodeContents(title);
    const t = range.getBoundingClientRect();
    // The price as it shows: the struck price when there is one, else the price itself
    const priceText = card.querySelector('.kc-plan-compare') || card.querySelector('.loop-subscription-group-price-amount');
    const priceRange = document.createRange(); priceRange.selectNodeContents(priceText);
    const price = priceRange.getBoundingClientRect();
    const border = parseFloat(getComputedStyle(card).borderTopWidth);
    ribbon = {
      text: band.textContent, w: Math.round(b.width), h: Math.round(b.height),
      centreOnBorder: +((b.top + b.height / 2) - (c.top + border / 2)).toFixed(1),
      gapToTitleEnd: Math.round(b.left - t.right), gapToPriceStart: Math.round(price.left - b.right),
    };
  }
  return { cta: box.querySelector('.kc-cta-label').textContent.trim(), promises, twice, ribbon };
})())"""


def orca(*args):
    out = subprocess.run(['orca', *args, '--page', PAGE, '--json'], capture_output=True, text=True, timeout=120)
    return json.loads(out.stdout)


def probe():
    for _ in range(2):
        orca('screenshot')
    return json.loads(orca('eval', '--expression', PROBE)['result']['result'])


PICK = """(() => { const box = document.querySelector('.kc-buybox');
  const link = box.querySelector('.kc-plan-link__btn');
  if (%(year)s && link && link.checkVisibility()) { link.click(); return 'link'; }
  const radios = Array.from(box.querySelectorAll('input[name=loop_purchase_option]'))
    .filter((r) => r.closest('.loop-one-time-purchase-option-position, .loop-subscription-group').checkVisibility());
  radios[%(index)d].click(); return 'radio'; })()"""

result = {}
for variant in VARIANTS:
    for width in (390, 1440):
        orca('goto', '--url', f'http://127.0.0.1:{PORT}/{variant}/en/products/karmicare-biorhythmic-oral-care-system')
        orca('viewport', '--width', str(width), '--height', '900', *(['--mobile'] if width < 750 else []))
        for _ in range(6):
            orca('screenshot')
        time.sleep(2.5)
        for state, index in (('once', 0), ('60day', 1), ('year', 2), ('once again', 0)):
            if state != 'once':
                orca('eval', '--expression', PICK % {'year': 'true' if state == 'year' else 'false', 'index': index})
                time.sleep(1.5)
            key = f'{variant} {width} {state}'
            result[key] = probe()
            print(key, json.dumps(result[key], ensure_ascii=False))
with open(OUT, 'w') as fh:
    json.dump(result, fh, indent=1, ensure_ascii=False)
