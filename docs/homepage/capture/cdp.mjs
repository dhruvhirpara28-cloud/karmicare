// Minimal CDP driver for headless Chrome (no dependencies; Node >= 22 WebSocket).
import { spawn } from 'node:child_process';
import { setTimeout as sleep } from 'node:timers/promises';

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

export async function launch({ port = 9333, profile }) {
  const proc = spawn(CHROME, [
    '--headless=new',
    `--remote-debugging-port=${port}`,
    `--user-data-dir=${profile}`,
    '--no-first-run',
    '--no-default-browser-check',
    '--hide-scrollbars',
    '--mute-audio',
    '--autoplay-policy=no-user-gesture-required',
    '--disable-background-timer-throttling',
    '--disable-renderer-backgrounding',
    '--disable-backgrounding-occluded-windows',
    '--disable-crash-reporter',
    '--disable-breakpad',
    // COMMON-RULES §4: only the store, cdn.shopify.com and Adobe Typekit.
    '--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE karmicares.myshopify.com, EXCLUDE cdn.shopify.com, EXCLUDE use.typekit.net, EXCLUDE p.typekit.net, EXCLUDE localhost, EXCLUDE 127.0.0.1',
    'about:blank',
  ], { stdio: ['ignore', 'ignore', 'pipe'] });
  let err = '';
  proc.stderr.on('data', (d) => { err += d; });
  for (let i = 0; i < 60; i++) {
    try {
      const r = await fetch(`http://127.0.0.1:${port}/json/version`);
      if (r.ok) return { proc, port };
    } catch {}
    await sleep(250);
  }
  proc.kill();
  throw new Error('Chrome did not start: ' + err.slice(0, 2000));
}

export async function newPage(port) {
  const r = await fetch(`http://127.0.0.1:${port}/json/new?about:blank`, { method: 'PUT' });
  const t = await r.json();
  return connect(t.webSocketDebuggerUrl);
}

function connect(url) {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(url);
    let id = 0;
    const pending = new Map();
    const listeners = new Map();
    ws.onmessage = (ev) => {
      const m = JSON.parse(ev.data);
      if (m.id && pending.has(m.id)) {
        const { res, rej } = pending.get(m.id);
        pending.delete(m.id);
        m.error ? rej(new Error(m.error.message)) : res(m.result);
      } else if (m.method && listeners.has(m.method)) {
        for (const fn of listeners.get(m.method)) fn(m.params);
      }
    };
    ws.onerror = reject;
    ws.onopen = () => {
      const page = {
        send(method, params = {}) {
          return new Promise((res, rej) => {
            const i = ++id;
            pending.set(i, { res, rej });
            ws.send(JSON.stringify({ id: i, method, params }));
          });
        },
        on(method, fn) {
          if (!listeners.has(method)) listeners.set(method, []);
          listeners.get(method).push(fn);
        },
        once(method, timeout = 30000) {
          return new Promise((res) => {
            const t = setTimeout(() => res(null), timeout);
            page.on(method, (p) => { clearTimeout(t); res(p); });
          });
        },
        async eval(expr) {
          const r = await page.send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true });
          if (r.exceptionDetails) throw new Error(JSON.stringify(r.exceptionDetails).slice(0, 800));
          return r.result.value;
        },
        close() { ws.close(); },
      };
      resolve(page);
    };
  });
}
