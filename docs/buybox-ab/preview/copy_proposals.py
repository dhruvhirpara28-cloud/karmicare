"""The copy proposals of PLAN.md section 4b (VOORSTEL, EN only) as the preview's /copy/ and /full/
variants apply them: what a Loop admin change (plan descriptions, plan option text) and a kc.receipt key
change would deliver, plus the Year's "per Duo" line, which has no source yet (copy-overlay.js).
Nothing is said twice in the buybox (Victor, 24 Nov): the money-back guarantee and pause / stop are in
the promises under the CTA (per plan), Care Credit in the chip, so the card lists leave them out."""
import json
import re

PID = '15977093923197'
RHYTHM_PLAN = '712106115453'
YEAR_PLAN = '712155431293'

# Same hooks as Loop's descriptions today: kc-dynamic_price (Care Credit % -> €), info-tip, the Welcome
# Kit pill and thumbnails, kc-bottom_label (Year badge)
RHYTHM_DESCRIPTION = """<div class="block__loop-description">
 <div class="kc-return_care-tooltip">
     <div class="kc-return_care">
      <span class="kc-dynamic_price">10%</span> Care Credit back, to spend on more care
       <span class="info-tip"><span class="info-icon">i</span><span class="info-tip-popover">10% of every 60-day supply comes back to you as Care Credit, in euros, to spend on member products and accessories. We believe prevention should pay the person doing the caring.</span></span>
      </div>
  </div>
  <div class="kc-description-list">
<span class="arrow">✓</span> <strong>1 Duo</strong>, Awake + Asleep, for 60 days</div>
  <div class="kc-description-list">
<span class="arrow">✓</span> <strong>An email 5 days before</strong> every renewal</div>
  <div class="kc-description-list">
<span class="arrow">✓</span> <strong>Your price stays the same</strong> while you stay</div>
  <div class="kc-description-list">
<span class="arrow">✓</span> <strong>Welcome Kit</strong> with your first order <span class="kc-welcome-kit-parent"><span class="dynamic_free_welcome_price">€21</span> value · free</span>
</div>
  <div class="block__show-welcome-kit"></div>
</div>
"""

YEAR_DESCRIPTION = """<div class="block__loop-description">
  <div class="kc-return_care-tooltip">
    <div class="kc-return_care">
      <span class="kc-dynamic_price">20%</span> Care Credit back, to spend on more care
      <span class="info-tip"><span class="info-icon">i</span><span class="info-tip-popover">The Year earns 20% in Care Credit, twice the 60-Day rate, in euros, to spend on member products and accessories. We believe prevention should pay the person doing the caring.</span></span>
    </div>
    <div class="kc-return_care">
      €40 Care Credit after a dental check-up from month 6
      <span class="info-tip"><span class="info-icon">i</span><span class="info-tip-popover">Complete a dental check-up from month 6 or onwards. €40 in Care Credit is added to your account. Prevention, rewarded.</span></span>
    </div>
  </div>
  <div class="kc-description-list">
<span class="arrow">✓</span> <strong>An email 30 and 7 days before</strong> your renewal</div>
  <div class="kc-description-list">
<span class="arrow">✓</span> <strong>Your price stays the same</strong> while you stay</div>
  <div class="kc-description-list">
<span class="arrow">✓</span> <strong>Welcome Kit</strong> with your first order <span class="kc-welcome-kit-parent"><span class="dynamic_free_welcome_price">€21</span> value · free</span>
</div>
  <div class="block__show-welcome-kit kc-wel-kit-bottom"></div>
  <div class="kc-bottom_label"></div>
</div>
"""

RHYTHM_OPTION = 'A new Duo every 60 days'
YEAR_SUBROW = '6 Duos a year, 3 now and 3 in month 6'


def apply(page):
    # 1. Plan descriptions in Loop's product JSON (buybox and end CTA), as Loop admin would deliver them
    pattern = r'(<script class="loopProductQuickJson-' + PID + r'" type="application/json">)(.*?)(</script>)'
    count = 0

    def replace_json(match):
        nonlocal count
        product = json.loads(match.group(2))
        for group in product['selling_plan_groups']:
            for plan in group['selling_plans']:
                if str(plan['id']) == RHYTHM_PLAN:
                    plan['description'] = RHYTHM_DESCRIPTION
                    count += 1
                elif str(plan['id']) == YEAR_PLAN:
                    plan['description'] = YEAR_DESCRIPTION
                    count += 1
        return match.group(1) + json.dumps(product, ensure_ascii=False) + match.group(3)

    page = re.sub(pattern, replace_json, page, flags=re.S)
    assert count == 4, f'plan descriptions replaced: {count}'

    # 2. 60-Day sub-row: Loop's plan option text (loop-widget.js shows it, "ships" -> "Renews")
    page, n = re.subn(r'(value="' + RHYTHM_PLAN + r'"[^>]*>\s*)ships every 60 days', r'\g<1>' + RHYTHM_OPTION, page)
    assert n == 2, f'60-Day option texts: {n}'

    # 3. Year sub-row: kc.receipt.renews_year on the receipt
    page, n = re.subn(r'data-kc-renews-year="Renews every year"', f'data-kc-renews-year="{YEAR_SUBROW}"', page)
    assert n == 1, f'renews_year: {n}'

    # 4. Year "€59 per Duo, billed once a year": no source yet, drawn by the preview overlay
    page = page.replace('</body>', '<script src="/assets/copy-overlay.js"></script></body>', 1)
    return page
