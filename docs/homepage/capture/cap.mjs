// Capture the live homepage per section at exact viewports, Day and Night.
// Usage: node cap.mjs <config.json>
// config: { url, out, tag, profile, port, viewports:[393,...], modes:["day","night"],
//           sections:[keys] (optional filter), overrides:{assetName: localPath}, injectCss: path|null,
//           metrics: path|null, full: bool, hover: selector|null }
import { launch, newPage } from './cdp.mjs';
import { writeFileSync, mkdirSync, readFileSync } from 'node:fs';
import { setTimeout as sleep } from 'node:timers/promises';

const cfg = JSON.parse(readFileSync(process.argv[2], 'utf8'));
mkdirSync(cfg.out, { recursive: true });

const VP = {
  393: { h: 852, dpr: 3, touch: true },
  450: { h: 900, dpr: 3, touch: true },
  768: { h: 1024, dpr: 2, touch: true },
  1024: { h: 768, dpr: 2, touch: false },
  1440: { h: 900, dpr: 2, touch: false },
  1920: { h: 1080, dpr: 1, touch: false },
  2560: { h: 1440, dpr: 1, touch: false },
};

const NAMES = [
  ['announcement-bar', 'announcement'], ['__header', 'header'], ['hero_karmicare', 'hero'],
  ['stat_strip', 'stat-strip'], ['chronobiology_clock', 'clock'], ['two_formulas', 'two-formulas'],
  ['product_benefits', 'benefits'], ['trusted_professionals', 'professionals'],
  ['research_behind_system', 'research'], ['care_comes_back', 'care-comes-back'],
  ['km_faq_accordion', 'faq'], ['featured_product', 'featured-product'], ['__footer', 'footer'],
];

const injectCss = cfg.injectCss ? readFileSync(cfg.injectCss, 'utf8') : null;
const injectJs = cfg.injectJs ? readFileSync(cfg.injectJs, 'utf8') : null;
const overrides = Object.fromEntries(Object.entries(cfg.overrides || {}).map(([k, v]) => [k, readFileSync(v)]));

const METRICS_JS = readFileSync(new URL('./metrics.js', import.meta.url), 'utf8');

const { proc, port } = await launch({ profile: cfg.profile, port: cfg.port || 9333 });
const allMetrics = {};
try {
  for (const vw of cfg.viewports) {
    const v = VP[vw];
    const p = await newPage(port);
    await p.send('Page.enable');
    await p.send('Runtime.enable');
    if (Object.keys(overrides).length) {
      await p.send('Fetch.enable', { patterns: Object.keys(overrides).map((n) => ({ urlPattern: `*assets/${n}*`, requestStage: 'Request' })) });
      p.on('Fetch.requestPaused', async (e) => {
        const name = Object.keys(overrides).find((n) => e.request.url.includes(`assets/${n}`));
        const body = overrides[name];
        const type = name.endsWith('.css') ? 'text/css' : name.endsWith('.js') ? 'application/javascript' : 'application/octet-stream';
        await p.send('Fetch.fulfillRequest', {
          requestId: e.requestId, responseCode: 200,
          responseHeaders: [{ name: 'Content-Type', value: type }, { name: 'Cache-Control', value: 'no-store' }],
          body: body.toString('base64'),
        });
      });
    }
    await p.send('Network.enable');
    await p.send('Network.setCacheDisabled', { cacheDisabled: true });
    await p.send('Emulation.setDeviceMetricsOverride', { width: vw, height: v.h, deviceScaleFactor: v.dpr, mobile: v.touch });
    await p.send('Emulation.setTouchEmulationEnabled', v.touch ? { enabled: true, maxTouchPoints: 5 } : { enabled: false });
    await p.send('Emulation.setEmulatedMedia', { features: [
      { name: 'hover', value: v.touch ? 'none' : 'hover' },
      { name: 'pointer', value: v.touch ? 'coarse' : 'fine' },
      { name: 'any-hover', value: v.touch ? 'none' : 'hover' },
      { name: 'any-pointer', value: v.touch ? 'coarse' : 'fine' },
    ] });
    const loaded = p.once('Page.loadEventFired', 60000);
    await p.send('Page.navigate', { url: cfg.url });
    await loaded;
    await sleep(2500);
    if (injectCss) {
      await p.eval(`(() => { const s = document.createElement('style'); s.id = 'kc-inject'; s.textContent = ${JSON.stringify(injectCss)}; document.body.appendChild(s); })()`);
    }
    if (injectJs) {
      await p.eval(injectJs);
      await sleep(500);
    }
    // Scroll through to trigger lazy images and reveal observers, then back to top.
    const H = await p.eval('document.documentElement.scrollHeight');
    for (let y = 0; y < H; y += Math.round(v.h * 0.7)) {
      await p.eval(`window.scrollTo(0, ${y})`);
      await sleep(180);
    }
    await p.eval('window.scrollTo(0, document.documentElement.scrollHeight)');
    await sleep(800);
    await p.eval('window.scrollTo(0, 0)');
    await sleep(800);
    // Wait for images.
    await p.eval(`Promise.race([Promise.all([...document.images].filter(i => !i.complete && i.loading !== 'lazy').map(i => new Promise(r => { i.onload = i.onerror = r; }))), new Promise(r => setTimeout(r, 6000))])`);

    for (const mode of cfg.modes) {
      await p.eval(`(() => {
        let b = document.getElementById('kc-cap-${mode}');
        if (!b) { b = document.createElement('button'); b.id = 'kc-cap-${mode}'; b.className = 'kc_${mode}'; b.hidden = true; document.body.appendChild(b); }
        b.click();
        if (!document.body.classList.contains('${mode}-mode')) { document.body.classList.remove('day-mode', 'night-mode'); document.body.classList.add('${mode}-mode'); }
      })()`);
      await sleep(1200);
      if (cfg.hover) {
        // Force hover-state for a selector via CDP (first match per section handled by caller CSS instead).
      }
      await p.eval(`document.getAnimations().forEach(a => { try { if (a.effect && a.effect.getComputedTiming().iterations !== Infinity) a.finish(); } catch (e) {} })`);
      await sleep(300);
      const info = JSON.parse(await p.eval(`(${METRICS_JS})(${vw}, ${v.dpr}, ${JSON.stringify(mode)})`));
      allMetrics[`${vw}-${mode}`] = info;
      for (const s of info.sections) {
        const short = (NAMES.find(([k]) => s.id.includes(k)) || [null, s.id])[1];
        s.short = short;
        if (cfg.sections && !cfg.sections.includes(short)) continue;
        if (s.height < 2) continue;
        const shot = await p.send('Page.captureScreenshot', {
          format: 'png', captureBeyondViewport: true,
          clip: { x: 0, y: s.top, width: vw, height: Math.min(s.height, 16000), scale: 1 / v.dpr },
        });
        writeFileSync(`${cfg.out}/${short}-${vw}-${mode}-${cfg.tag}.png`, Buffer.from(shot.data, 'base64'));
      }
      if (cfg.full) {
        const fullH = await p.eval('document.documentElement.scrollHeight');
        const scale = Math.min(1, 720 / vw) / v.dpr;
        const shot = await p.send('Page.captureScreenshot', {
          format: 'png', captureBeyondViewport: true,
          clip: { x: 0, y: 0, width: vw, height: fullH, scale },
        });
        writeFileSync(`${cfg.out}/page-${vw}-${mode}-${cfg.tag}.png`, Buffer.from(shot.data, 'base64'));
      }
    }
    p.close();
    console.log('done', vw);
  }
} finally {
  if (cfg.metrics) writeFileSync(cfg.metrics, JSON.stringify(allMetrics, null, 1));
  proc.kill();
}
