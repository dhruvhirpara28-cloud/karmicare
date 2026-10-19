#!/usr/bin/env node
// Measure the live homepage or Duo PDP at the A3 viewports in headless Chrome, with or
// without assets/kc-fluid.css, and save per-section screenshots.
//
//   node docs/utopia/tools/measure.mjs --page home --label before --attr --shots
//   node docs/utopia/tools/measure.mjs --page home --label after --css assets/kc-fluid.css --shots
//
// --css appends that file to the kc-tokens.css response (Fetch domain), which puts it in
// the cascade exactly where `{{ 'kc-fluid.css' | asset_url | stylesheet_tag }}` right after
// kc-tokens.css would. Read-only against the store: GET requests only, nothing is clicked
// except an injected .kc_day / .kc_night control (assets/day-night-mode.js keeps the mode
// in memory, nothing is stored). Needs Google Chrome and Node 22+ (global WebSocket).
import { spawn } from 'node:child_process';
import { mkdirSync, mkdtempSync, readFileSync, writeFileSync, existsSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const STORE = 'https://karmicares.myshopify.com';
const PAGES = {
  home: STORE + '/',
  pdp: STORE + '/products/karmicare-biorhythmic-oral-care-system',
};
const HEIGHTS = { 393: 852, 450: 900, 768: 1024, 1024: 768, 1440: 900, 1920: 1080, 2560: 1440 };

const args = process.argv.slice(2);
const opt = (name, dflt) => {
  const i = args.indexOf('--' + name);
  return i === -1 ? dflt : args[i + 1];
};
const flag = (name) => args.includes('--' + name);
const page = opt('page', 'home');
const label = opt('label', 'before');
const cssPath = opt('css', null);
const widths = opt('widths', '393,768,1024,1440,1920,2560').split(',').map(Number);
const doAttr = flag('attr');
const doShots = flag('shots');
const nightHero = flag('night-hero');
const outDir = path.join(ROOT, 'docs/utopia');
// --css takes one path or a comma-separated list, appended in that order.
const injectCss = cssPath
  ? cssPath.split(',').map((p) => `/* ${p} */\n` + readFileSync(path.resolve(ROOT, p), 'utf8')).join('\n')
  : null;
const probeSrc = readFileSync(path.join(ROOT, 'docs/utopia/tools/probe.js'), 'utf8');

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

class CDP {
  constructor(url) {
    this.ws = new WebSocket(url);
    this.seq = 0;
    this.pending = new Map();
    this.handlers = new Map();
    this.ws.addEventListener('message', (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.id) {
        const p = this.pending.get(msg.id);
        if (!p) return;
        this.pending.delete(msg.id);
        if (msg.error) p.reject(new Error(`${p.method}: ${msg.error.message}`));
        else p.resolve(msg.result);
      } else {
        for (const fn of this.handlers.get(msg.method) || []) fn(msg.params);
      }
    });
  }
  open() {
    return new Promise((resolve, reject) => {
      this.ws.addEventListener('open', resolve, { once: true });
      this.ws.addEventListener('error', reject, { once: true });
    });
  }
  send(method, params = {}) {
    const id = ++this.seq;
    this.ws.send(JSON.stringify({ id, method, params }));
    return new Promise((resolve, reject) => this.pending.set(id, { resolve, reject, method }));
  }
  on(method, fn) {
    if (!this.handlers.has(method)) this.handlers.set(method, []);
    this.handlers.get(method).push(fn);
  }
  waitFor(method, timeout = 45000) {
    return new Promise((resolve, reject) => {
      const t = setTimeout(() => reject(new Error('timeout waiting for ' + method)), timeout);
      const fn = (p) => {
        clearTimeout(t);
        this.handlers.set(method, (this.handlers.get(method) || []).filter((f) => f !== fn));
        resolve(p);
      };
      this.on(method, fn);
    });
  }
}

async function launch() {
  const dataDir = mkdtempSync(path.join(tmpdir(), 'utopia-chrome-'));
  const proc = spawn(CHROME, [
    '--headless=new', '--remote-debugging-port=0', `--user-data-dir=${dataDir}`,
    '--no-first-run', '--no-default-browser-check', '--disable-breakpad', '--hide-scrollbars',
    '--mute-audio', '--autoplay-policy=no-user-gesture-required', 'about:blank',
  ], { stdio: 'ignore' });
  const portFile = path.join(dataDir, 'DevToolsActivePort');
  for (let i = 0; i < 100 && !existsSync(portFile); i++) await sleep(100);
  const port = readFileSync(portFile, 'utf8').split('\n')[0];
  let target;
  for (let i = 0; i < 50 && !target; i++) {
    const list = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
    target = list.find((t) => t.type === 'page');
    if (!target) await sleep(100);
  }
  const cdp = new CDP(target.webSocketDebuggerUrl);
  await cdp.open();
  const close = async () => {
    const exited = new Promise((r) => proc.once('exit', r));
    proc.kill();
    await Promise.race([exited, sleep(5000)]);
    try {
      rmSync(dataDir, { recursive: true, force: true, maxRetries: 5, retryDelay: 200 });
    } catch (e) {
      console.warn('could not remove', dataDir, e.code);
    }
  };
  return { cdp, close };
}

// --- source maps: minified CDN CSS back to the repo file and line ---------------------
const B64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
function decodeMappings(str) {
  const lines = [];
  let src = 0, sLine = 0, sCol = 0;
  for (const lineStr of str.split(';')) {
    const segs = [];
    let gCol = 0;
    if (lineStr) {
      for (const seg of lineStr.split(',')) {
        const vals = [];
        let shift = 0, value = 0;
        for (const ch of seg) {
          let d = B64.indexOf(ch);
          const cont = d & 32;
          d &= 31;
          value += d << shift;
          if (cont) shift += 5;
          else {
            vals.push(value & 1 ? -(value >> 1) : value >> 1);
            value = 0;
            shift = 0;
          }
        }
        gCol += vals[0];
        if (vals.length >= 4) {
          src += vals[1]; sLine += vals[2]; sCol += vals[3];
          segs.push([gCol, src, sLine, sCol]);
        }
      }
    }
    lines.push(segs);
  }
  return lines;
}

const sheets = new Map();
const maps = new Map();
async function originalPosition(sheetId, line, col) {
  const h = sheets.get(sheetId);
  if (!h) return null;
  if (h.isInline || !h.sourceMapURL) return { file: h.isInline ? 'inline' : h.sourceURL, line: null };
  const mapUrl = new URL(h.sourceMapURL, h.sourceURL).href;
  if (!maps.has(mapUrl)) {
    try {
      const m = await (await fetch(mapUrl)).json();
      maps.set(mapUrl, { sources: m.sources, lines: decodeMappings(m.mappings) });
    } catch {
      maps.set(mapUrl, null);
    }
  }
  const m = maps.get(mapUrl);
  if (!m) return { file: h.sourceURL, line: null };
  let best = null;
  for (const s of m.lines[line] || []) {
    if (s[0] <= col) best = s;
    else break;
  }
  if (!best) return { file: h.sourceURL, line: null };
  return { file: m.sources[best[1]].replace(/^\/cdn\/shop\/t\/\d+\//, ''), line: best[2] + 1 };
}

function pickDecl(styles, name) {
  // Cascade order within one element: matched rules ascend in precedence, inline last;
  // !important beats normal.
  let win = null;
  const consider = (decl, rule, inline) => {
    if (win && win.important && !decl.important) return;
    win = { value: decl.value, important: !!decl.important, range: decl.range || rule?.style?.range,
      sheet: rule?.styleSheetId || (inline ? 'inline-attr' : null), selector: rule?.selectorList?.text || 'style=""',
      origin: rule?.origin || 'inline', media: (rule?.media || []).map((m) => m.text).join(' | ') };
  };
  for (const m of styles.matchedCSSRules || []) {
    for (const d of m.rule.style.cssProperties) {
      if (d.name === name && d.parsedOk !== false && !d.disabled) consider(d, m.rule, false);
    }
  }
  for (const d of styles.inlineStyle?.cssProperties || []) {
    if (d.name === name && d.parsedOk !== false && !d.disabled && d.text) consider(d, null, true);
  }
  return win;
}

async function attribute(cdp) {
  const { root } = await cdp.send('DOM.getDocument', { depth: 0 });
  const { nodeIds } = await cdp.send('DOM.querySelectorAll', { nodeId: root.nodeId, selector: '[data-u-i]' });
  const result = {};
  for (const nodeId of nodeIds) {
    const { attributes } = await cdp.send('DOM.getAttributes', { nodeId });
    const i = attributes[attributes.indexOf('data-u-i') + 1];
    const styles = await cdp.send('CSS.getMatchedStylesForNode', { nodeId });
    const entry = {};
    for (const prop of ['font-size', 'line-height']) {
      let win = pickDecl(styles, prop);
      let depth = 0;
      if (!win) {
        for (const anc of styles.inherited || []) {
          depth++;
          win = pickDecl(anc, prop);
          if (win) break;
        }
      }
      if (!win) continue;
      const pos = win.range && win.sheet && win.sheet !== 'inline-attr'
        ? await originalPosition(win.sheet, win.range.startLine, win.range.startColumn) : null;
      entry[prop] = { value: win.value, selector: win.selector.slice(0, 160), origin: win.origin, media: win.media,
        inheritedDepth: depth, file: pos?.file || (win.sheet === 'inline-attr' ? 'style attribute' : null), line: pos?.line || null };
    }
    result[i] = entry;
  }
  return result;
}

async function evaluate(cdp, expression, awaitPromise = false) {
  const r = await cdp.send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise });
  if (r.exceptionDetails) throw new Error('page error: ' + JSON.stringify(r.exceptionDetails).slice(0, 400));
  return r.result.value;
}

const SETTLE = `(async () => {
  const step = Math.round(innerHeight * 0.8);
  for (let y = 0; y < document.documentElement.scrollHeight; y += step) {
    window.scrollTo(0, y);
    await new Promise((r) => setTimeout(r, 140));
  }
  window.scrollTo(0, 0);
  await new Promise((r) => setTimeout(r, 600));
  document.querySelectorAll('video').forEach((v) => { try { v.pause(); v.currentTime = Math.min(1.5, v.duration || 1.5); } catch (e) {} });
  document.getAnimations().forEach((a) => { try { a.finish(); } catch (e) {} });
  await document.fonts.ready;
  return document.fonts.size;
})()`;

const setMode = (mode) => `(async () => {
  const b = document.createElement('button');
  b.className = 'kc_${mode}';
  b.style.display = 'none';
  document.body.appendChild(b);
  b.click();
  b.remove();
  await new Promise((r) => setTimeout(r, 900));
  document.getAnimations().forEach((a) => { try { a.finish(); } catch (e) {} });
  return document.body.className;
})()`;

const HIDE_OVERLAYS = `(() => {
  const s = document.createElement('style');
  s.id = 'utopia-shot-hide';
  s.textContent = '#shopify-pc__banner, #shopify-pc__prefs__dialog, #stickyCta, .sticky-cta { display: none !important; }';
  document.head.appendChild(s);
  return true;
})()`;

async function screenshot(cdp, file, clip) {
  const { data } = await cdp.send('Page.captureScreenshot', { format: 'png', clip: { ...clip, scale: 1 }, captureBeyondViewport: true });
  writeFileSync(file, Buffer.from(data, 'base64'));
}

async function run() {
  const { cdp, close } = await launch();
  const results = { page, label, css: cssPath, measured: new Date().toISOString(), viewports: [] };
  try {
    cdp.on('CSS.styleSheetAdded', ({ header }) => sheets.set(header.styleSheetId, header));
    await cdp.send('Page.enable');
    await cdp.send('Runtime.enable');
    await cdp.send('Network.enable');
    await cdp.send('Network.setCacheDisabled', { cacheDisabled: true });
    if (injectCss) {
      await cdp.send('Fetch.enable', { patterns: [{ urlPattern: '*kc-tokens.css*', resourceType: 'Stylesheet', requestStage: 'Response' }] });
      cdp.on('Fetch.requestPaused', async (ev) => {
        try {
          const body = await cdp.send('Fetch.getResponseBody', { requestId: ev.requestId });
          const text = body.base64Encoded ? Buffer.from(body.body, 'base64').toString('utf8') : body.body;
          const merged = text + '\n/* utopia: assets/kc-fluid.css appended by measure.mjs */\n' + injectCss;
          await cdp.send('Fetch.fulfillRequest', { requestId: ev.requestId, responseCode: ev.responseStatusCode || 200,
            responseHeaders: (ev.responseHeaders || []).filter((h) => !/^content-length$/i.test(h.name)),
            body: Buffer.from(merged, 'utf8').toString('base64') });
        } catch (e) {
          await cdp.send('Fetch.continueRequest', { requestId: ev.requestId }).catch(() => {});
        }
      });
    }
    const shotDir = path.join(outDir, 'shots', page);
    if (doShots) mkdirSync(shotDir, { recursive: true });

    for (const w of widths) {
      const h = HEIGHTS[w] || 900;
      const mobile = w < 1024;
      await cdp.send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: 1, mobile });
      await cdp.send('Emulation.setTouchEmulationEnabled', { enabled: mobile });
      if (doAttr) { await cdp.send('DOM.disable').catch(() => {}); await cdp.send('CSS.disable').catch(() => {}); }
      sheets.clear();
      const loaded = cdp.waitFor('Page.loadEventFired', 60000);
      await cdp.send('Page.navigate', { url: PAGES[page] });
      await loaded;
      if (doAttr) { await cdp.send('DOM.enable'); await cdp.send('CSS.enable'); }
      await sleep(1500);
      const theme = await evaluate(cdp, 'JSON.stringify(window.Shopify && Shopify.theme && { id: Shopify.theme.id, name: Shopify.theme.name })');
      const bodyClass = await evaluate(cdp, setMode('day'), true);
      const fonts = await evaluate(cdp, SETTLE, true);
      const injected = await evaluate(cdp, `getComputedStyle(document.documentElement).getPropertyValue('--kc-responsive-body-md-text-size')`);
      const data = await evaluate(cdp, probeSrc);
      data.theme = JSON.parse(theme || 'null');
      data.bodyClass = bodyClass;
      data.fontFaces = fonts;
      data.bodyMdToken = injected.trim();
      if (doAttr) data.attribution = await attribute(cdp);
      if (doShots) {
        await evaluate(cdp, HIDE_OVERLAYS);
        for (const s of data.sections) {
          if (s.height < 2) continue;
          const file = path.join(shotDir, `${s.name}-${w}-day-${label}.png`);
          await evaluate(cdp, `window.scrollTo(0, ${s.top}); new Promise((r) => setTimeout(r, 250))`, true);
          await screenshot(cdp, file, { x: 0, y: s.top, width: w, height: Math.min(s.height, 6000) });
        }
        if (nightHero && data.sections.length) {
          // Homepage: hero_karmicare; PDP: the main product section (named "main").
          const hero = data.sections.find((s) => /^hero|^main$|main[-_]product/.test(s.name) && s.height > 200)
            || data.sections.find((s) => s.height > 200);
          await evaluate(cdp, 'window.scrollTo(0, 0)');
          await evaluate(cdp, setMode('night'), true);
          await screenshot(cdp, path.join(shotDir, `${hero.name}-${w}-night-${label}.png`), { x: 0, y: hero.top, width: w, height: Math.min(hero.height, 6000) });
          await evaluate(cdp, setMode('day'), true);
        }
      }
      results.viewports.push(data);
      console.log(`${page} ${label} ${w}: ${data.texts.length} texts, ${data.sections.length} sections, theme ${theme}, body-md token ${data.bodyMdToken}, overflow ${data.horizontalOverflow}`);
    }
    mkdirSync(path.join(outDir, 'data'), { recursive: true });
    const file = path.join(outDir, 'data', `${page}-${label}.json`);
    writeFileSync(file, JSON.stringify(results));
    console.log('wrote', path.relative(ROOT, file));
  } finally {
    await close();
  }
}

run().catch((e) => {
  console.error(e);
  process.exit(1);
});
