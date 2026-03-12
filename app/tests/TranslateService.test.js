import { test } from 'node:test';
import assert from 'node:assert/strict';
import { config } from '../utils/config.js';


async function canReachTranslate() {
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 5000);
    const res = await fetch(config.getTranslateApiEndpoint(), { method: 'OPTIONS', signal: controller.signal });
    clearTimeout(timeout);
    return { ok: !!res, status: res?.status };
  } catch (e) {
    return { ok: false, error: e?.message || String(e) };
  }
}

test('Translate API endpoint builds', () => {
  const url = config.getTranslateApiEndpoint();
  assert.ok(url.includes('http'));
});

test('LibreTranslate translation (integration)', async () => {
  const ping = await canReachTranslate();
  if (!ping.ok) {
    const url = config.getTranslateApiEndpoint();
    const extra = ping.error ? `Error: ${ping.error}` : `HTTP ${ping.status}`;
    assert.fail(`Translate service not reachable at ${url}. ${extra}`);
  }

  const payload = { q: 'Hello world', source: 'en', target: 'de', format: 'text', alternatives: 0 };
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 8000);
  
  try {
    const res = await fetch(config.getTranslateApiEndpoint(), {
      method: 'POST', 
      headers: { 'Content-Type': 'application/json' }, 
      body: JSON.stringify(payload), 
      signal: controller.signal
    });
    
    assert.ok(res.ok, `HTTP ${res.status}: ${res.statusText}`);
    const body = await res.json();
    assert.ok(typeof body.translatedText === 'string', 'Response should contain translatedText as string');
    assert.ok(body.translatedText.length > 0, 'Translation should not be empty');
    
    // Basic validation that translation happened (not same as input)
    assert.notStrictEqual(body.translatedText, payload.q, 'Translation should be different from input');
  } finally {
    clearTimeout(timeout);
  }
});
